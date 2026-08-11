"""Parse the 98 mental-model markdown files into ``Model`` records.

This module is the **single** implementation of the markdown section parser.
``catalog``, ``search``, ``render``, ``cli``, the MCP server, ``scripts/`` and the
evals all import from here. Do not copy the regex block anywhere else.

Content-root resolution order (see BUILD-SPEC 1.2):

1. Explicit override -- ``set_content_root(path)`` / ``--content-root PATH``.
2. Bundled package data -- ``mental_models_kit/data/models`` (real wheel install).
3. Walk up from ``__file__`` for ``skills/mental-models/models`` (editable install
   and in-repo development; ``uv pip install -e`` does not materialise
   force-included package data, so this tier is load-bearing).

There is deliberately **no** cwd walk-up tier and **no** environment variable:
CLI behaviour must not depend on the directory you invoke it from.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Callable, NamedTuple

__all__ = [
    "CATEGORIES",
    "Category",
    "ContentRootNotFound",
    "Model",
    "ModelNotFound",
    "UnknownCategory",
    "clear_caches",
    "get_model",
    "list_categories",
    "list_models",
    "load_models",
    "models_root",
    "normalize_slug",
    "parse_markdown",
    "register_cache_clearer",
    "resolve_category",
    "set_content_root",
    "skill_root",
]


# --------------------------------------------------------------------------
# Errors
# --------------------------------------------------------------------------


class ContentRootNotFound(RuntimeError):
    """The directory holding the model markdown files could not be located."""


class ModelNotFound(KeyError):
    """No model matches the requested slug or id."""

    def __str__(self) -> str:  # KeyError repr-quotes its arg; we want the message
        return self.args[0] if self.args else ""


class UnknownCategory(ValueError):
    """The requested category is not one of the eight canonical categories."""


# --------------------------------------------------------------------------
# Categories -- derived from the directory, not from the **Category = ...** line.
#
# Five War models each carry a unique "Warfare & X" string; trusting the line
# yields 12 categories and makes `list --category "Warfare & Strategy"` return 0
# results for four of them. The raw string is preserved as ``category_detail``.
# ORDER IS THE CANONICAL ORDER and is load-bearing for CATALOG.md determinism.
# --------------------------------------------------------------------------

CATEGORIES: tuple[tuple[str, str, str, int], ...] = (
    ("general", "General Thinking Tools", "Mental_Model_General", 9),
    ("science", "Physics, Chemistry, and Biology", "Mental_Model_Science", 20),
    ("math", "Mathematics", "Mental_Model_Math", 7),
    ("economics", "Economics", "Mental_Model_Economics", 12),
    ("systems", "Systems Thinking", "Mental_Model_SysThinking", 11),
    ("art", "Art", "Mental_Model_Art", 11),
    ("war", "Warfare & Strategy", "Mental_Model_War", 5),
    ("human-nature", "Human Nature & Judgment", "Mental_Model_HumanNature", 23),
)

_CATEGORY_ORDER = {key: i for i, (key, _d, _dir, _n) in enumerate(CATEGORIES)}
_DIR_TO_CATEGORY = {d: (key, display) for key, display, d, _n in CATEGORIES}


class Category(NamedTuple):
    key: str
    display: str
    count: int


# --------------------------------------------------------------------------
# The parser -- ONE implementation, order-independent.
# --------------------------------------------------------------------------

_LABELS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("description", re.compile(r"\*\*Description:\*\*", re.I)),
    ("when_to_avoid", re.compile(r"\*\*When to Avoid[^*]*:\*\*", re.I)),
    ("keywords", re.compile(r"\*\*Keywords[^*]*:\*\*", re.I)),
    ("thinking_steps", re.compile(r"\*\*Thinking Steps:\*\*", re.I)),
    ("coaching_questions", re.compile(r"\*\*Coaching Questions:\*\*", re.I)),
)
_NAME = re.compile(r"^##\s*Mental Model\s*=\s*(.+)$", re.M)
_CATEGORY_RAW = re.compile(r"^\*\*Category\s*=\s*(.+?)\*\*\s*$", re.M)

SECTION_NAMES: tuple[str, ...] = tuple(k for k, _ in _LABELS)


def parse_markdown(text: str) -> dict[str, str]:
    """Split one model file into its named parts.

    Returns a dict with ``name``, ``category_detail`` and the five section keys
    of :data:`SECTION_NAMES`. Missing pieces come back as ``""`` -- callers that
    need to *enforce* presence (``scripts/validate_corpus.py``) count the regex
    matches themselves.

    The scan is order-independent: every label is located, the hits are sorted by
    position, and each section runs to the start of the next one. Sub-headings
    inside a section (``**Clearly Define Your Goal:**``) are body text, not
    boundaries.
    """
    out: dict[str, str] = {"name": "", "category_detail": ""}
    for key in SECTION_NAMES:
        out[key] = ""
    if not text:
        return out

    m = _NAME.search(text)
    if m:
        out["name"] = m.group(1).strip()
    m = _CATEGORY_RAW.search(text)
    if m:
        out["category_detail"] = m.group(1).strip()

    hits: list[tuple[str, int, int]] = []
    for key, pat in _LABELS:
        found = pat.search(text)
        if found:
            hits.append((key, found.start(), found.end()))
    hits.sort(key=lambda h: h[1])
    for i, (key, _label_start, body_start) in enumerate(hits):
        body_end = hits[i + 1][1] if i + 1 < len(hits) else len(text)
        out[key] = text[body_start:body_end].strip()
    return out


def split_keywords(raw: str) -> tuple[str, ...]:
    """Turn the ``Keywords for Situations`` blob into an ordered tuple.

    Comma separated, file order preserved, trailing full stops removed.
    """
    out: list[str] = []
    for part in raw.replace("\n", " ").split(","):
        kw = part.strip().rstrip(".").strip()
        if kw:
            out.append(kw)
    return tuple(out)


# --------------------------------------------------------------------------
# Model
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Model:
    slug: str
    id: str
    name: str
    category: str
    category_key: str
    category_detail: str
    keywords: tuple[str, ...]
    description: str
    when_to_avoid: str
    thinking_steps: str
    coaching_questions: str
    path: str
    markdown: str = field(default="", repr=False, compare=False)


# --------------------------------------------------------------------------
# Slug normalisation
# --------------------------------------------------------------------------

_SEP_RE = re.compile(r"[-_\s]+")
_DROP_RE = re.compile(r"['’]")


def normalize_slug(value: str) -> str:
    """Fold a user-supplied identifier onto a canonical comparison key.

    ``hanlon's_razor``, ``hanlons-razor`` and ``Hanlons Razor`` all normalise to
    ``hanlons-razor``. Slugs on disk are inconsistent by design -- renaming the
    files would churn every public identifier for cosmetics.
    """
    s = _DROP_RE.sub("", (value or "").strip().casefold())
    return _SEP_RE.sub("-", s).strip("-")


# --------------------------------------------------------------------------
# Content root
# --------------------------------------------------------------------------

_REPO_RELATIVE_PREFIX = "skills/mental-models/models"
_MODELS_SUBPATH = ("skills", "mental-models", "models")

_override: Path | None = None
_CACHE_CLEARERS: list[Callable[[], None]] = []


def register_cache_clearer(fn: Callable[[], None]) -> Callable[[], None]:
    """Register a callable invoked by :func:`clear_caches`.

    ``search`` uses this so its token index cannot survive a content-root swap.
    """
    _CACHE_CLEARERS.append(fn)
    return fn


def clear_caches() -> None:
    load_models.cache_clear()
    _resolve_root.cache_clear()
    for fn in _CACHE_CLEARERS:
        fn()


def set_content_root(path: str | os.PathLike[str] | None) -> None:
    """Override the content root (or restore auto-detection with ``None``).

    Clears every cache. Intended for tests and for ``--content-root``.
    """
    global _override
    _override = Path(path).expanduser().resolve() if path is not None else None
    clear_caches()


@lru_cache(maxsize=1)
def _resolve_root() -> tuple[Path, str]:
    if _override is not None:
        return _override, "override"

    bundled = Path(__file__).resolve().parent / "data" / "models"
    if bundled.is_dir():
        return bundled, "bundled"

    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent.joinpath(*_MODELS_SUBPATH)
        if candidate.is_dir():
            return candidate, "repo"

    raise ContentRootNotFound(
        "Could not locate the mental-model markdown files. Tried, in order: "
        "(1) an explicit --content-root / set_content_root() override; "
        f"(2) bundled package data at {bundled}; "
        f"(3) a '{'/'.join(_MODELS_SUBPATH)}' directory in any parent of {here}. "
        "Reinstall the package, or pass --content-root pointing at a directory "
        "containing the Mental_Model_* folders."
    )


def models_root() -> Path:
    """Absolute path of the directory containing the ``Mental_Model_*`` folders."""
    return _resolve_root()[0]


def content_root_source() -> str:
    """``"override"``, ``"bundled"`` or ``"repo"`` -- how the root was found."""
    return _resolve_root()[1]


def skill_root() -> Path:
    """Directory holding ``SKILL.md`` and its sibling reference documents.

    In a wheel the skill docs live beside the models under ``data/skill``; in the
    repo they are the models' parent directory. Callers should check
    ``is_dir()`` -- an override root need not have skill docs at all.
    """
    root, source = _resolve_root()
    if source == "bundled":
        return root.parent / "skill"
    return root.parent


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------

_FILENAME_RE = re.compile(r"^(m\d{2})_(.+)\.md$")


@lru_cache(maxsize=1)
def load_models() -> tuple[Model, ...]:
    """Read and parse every model file. Cached; sorted by (category order, id)."""
    root = models_root()
    models: list[Model] = []
    for _key, _display, dirname, _n in CATEGORIES:
        directory = root / dirname
        if not directory.is_dir():
            continue
        for md_path in sorted(directory.glob("*.md")):
            if md_path.name == "_TEMPLATE.md":
                continue
            models.append(_build(md_path, dirname))
    models.sort(key=lambda m: (_CATEGORY_ORDER[m.category_key], m.id))
    return tuple(models)


def _build(md_path: Path, dirname: str) -> Model:
    text = md_path.read_text(encoding="utf-8")
    parsed = parse_markdown(text)
    fname = _FILENAME_RE.match(md_path.name)
    if fname:
        model_id, slug = fname.group(1), fname.group(2)
    else:  # tolerated so a malformed drop-in surfaces in validate_corpus, not here
        model_id, slug = "", md_path.stem
    cat_key, cat_display = _DIR_TO_CATEGORY[dirname]
    return Model(
        slug=slug,
        id=model_id,
        name=parsed["name"],
        category=cat_display,
        category_key=cat_key,
        category_detail=parsed["category_detail"],
        keywords=split_keywords(parsed["keywords"]),
        description=parsed["description"],
        when_to_avoid=parsed["when_to_avoid"],
        thinking_steps=parsed["thinking_steps"],
        coaching_questions=parsed["coaching_questions"],
        path=f"{_REPO_RELATIVE_PREFIX}/{dirname}/{md_path.name}",
        markdown=text,
    )


# --------------------------------------------------------------------------
# Lookup
# --------------------------------------------------------------------------


@lru_cache(maxsize=1)
def _lookup() -> dict[str, Model]:
    table: dict[str, Model] = {}
    for m in load_models():
        table.setdefault(normalize_slug(m.slug), m)
        if m.id:
            table.setdefault(m.id.casefold(), m)
    return table


register_cache_clearer(lambda: _lookup.cache_clear())


def get_model(key: str) -> Model:
    """Look up a model by slug, normalised slug, or id (``m07``)."""
    raw = (key or "").strip()
    if not raw:
        raise ModelNotFound("empty model key")
    table = _lookup()
    hit = table.get(normalize_slug(raw)) or table.get(raw.casefold())
    if hit is None:
        raise ModelNotFound(
            f"No model with slug or id {raw!r}. "
            "Run `mental-models catalog` for the 98 valid slugs."
        )
    return hit


def resolve_category(value: str) -> Category:
    """Resolve a category key or display name, case- and whitespace-tolerant.

    Raises :class:`UnknownCategory` -- never returns an empty result silently.
    """
    wanted = normalize_slug(value)
    for key, display, _dir, _n in CATEGORIES:
        if wanted in (normalize_slug(key), normalize_slug(display)):
            return Category(key, display, _n)
    valid = ", ".join(k for k, _d, _dir, _n in CATEGORIES)
    raise UnknownCategory(f"Unknown category {value!r}. Valid categories: {valid}")


def list_models(category: str | None = None) -> tuple[Model, ...]:
    models = load_models()
    if category is None:
        return models
    cat = resolve_category(category)
    return tuple(m for m in models if m.category_key == cat.key)


def list_categories() -> tuple[Category, ...]:
    """The eight canonical categories, in canonical order, with live counts."""
    counts: dict[str, int] = {}
    for m in load_models():
        counts[m.category_key] = counts.get(m.category_key, 0) + 1
    return tuple(
        Category(key, display, counts.get(key, 0))
        for key, display, _dir, _n in CATEGORIES
    )

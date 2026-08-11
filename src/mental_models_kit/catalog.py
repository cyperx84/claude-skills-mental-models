"""Compact-catalog renderers.

The catalog is the primary selection surface: the CLI/MCP hands the harness LLM
a compact list of every model, the model picks 2-4 slugs, and the CLI retrieves
those slugs exactly. Keyword matching (``search``) is a fallback, not the path.

Output is byte-deterministic -- ``skills/mental-models/CATALOG.md`` is gated in
CI with a byte diff against ``mental-models catalog --with-header``.
"""

from __future__ import annotations

from .corpus import Category, list_categories, list_models, resolve_category

__all__ = ["FORMATS", "catalog_document", "render_catalog"]

FORMATS = ("compact", "slim")

_HEADER_TITLE = "# Mental Models Catalog"


def _line(slug: str, name: str, keywords: tuple[str, ...], fmt: str) -> str:
    if fmt == "slim" or not keywords:
        return f"- `{slug}` — {name}"
    return f"- `{slug}` — {name}: {', '.join(keywords)}"


def render_catalog(fmt: str = "compact", category: str | None = None) -> str:
    """Render the catalog body (no header).

    ``compact`` includes every keyword (~17 KB, ~4.3k tokens); ``slim`` is
    slug + name only (~6 KB, ~1.5k tokens) for tight-context harnesses.
    """
    if fmt not in FORMATS:
        raise ValueError(
            f"Unknown catalog format {fmt!r}. Valid formats: {', '.join(FORMATS)}"
        )
    wanted: set[str] | None = None
    if category is not None:
        wanted = {resolve_category(category).key}

    chunks: list[str] = []
    for cat in list_categories():
        if wanted is not None and cat.key not in wanted:
            continue
        models = list_models(cat.key)
        chunks.append(f"## {cat.display} ({len(models)})\n")
        for m in models:
            chunks.append(_line(m.slug, m.name, m.keywords, fmt))
        chunks.append("")
    return "\n".join(chunks).rstrip("\n") + "\n"


def catalog_document(fmt: str = "compact", category: str | None = None) -> str:
    """Header + body. This is the exact byte content of ``CATALOG.md``."""
    body = render_catalog(fmt, category)
    if category is None:
        cats: tuple[Category, ...] = list_categories()
    else:
        cat = resolve_category(category)
        cats = tuple(c for c in list_categories() if c.key == cat.key)
    total = sum(c.count for c in cats)
    plural = "categories" if len(cats) != 1 else "category"
    header = (
        f"{_HEADER_TITLE}\n"
        "\n"
        f"{total} models in {len(cats)} {plural}. Pick 2-4 across different "
        "categories, then retrieve each by its\n"
        "exact slug: `mental-models get <slug>` (or read\n"
        "`skills/mental-models/models/<Category_Dir>/<mNN>_<slug>.md`).\n"
        "\n"
    )
    return header + body

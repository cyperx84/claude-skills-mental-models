#!/usr/bin/env python3
"""Validate the 98 model markdown files: real format checks plus the content
checksum gate.

The predecessor (``validate_models.py``) lowercased the whole file and
substring-searched, so the bare word "description" anywhere in the prose
satisfied the ``**Description:**`` gate. Its 98/0 green proved nothing. This
one matches the actual labels, exactly once each, and extracts the sections to
confirm they are non-empty.

Every failure is collected and reported; exit 1 if any.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from mental_models_kit.corpus import (  # noqa: E402
    CATEGORIES,
    _CATEGORY_RAW,
    _LABELS,
    _NAME,
    models_root,
    normalize_slug,
    parse_markdown,
)

#: sha256 of the sorted per-file sha256 list, excluding _TEMPLATE.md.
#: Invariant 1: the prose of the 98 files is never edited, only moved.
EXPECTED_CORPUS_SHA256 = "12f869084e3019de5f11e714c69c20f07525a6032ae642517ef51a898ca27ffe"
EXPECTED_TEMPLATE_SHA256 = "25ad23bbd1dd4dda195366c1420e3665012c303950755f1de935bb4864579b0b"

FILENAME_RE = re.compile(r"^m\d{2}_.+\.md$")
VALID_DIRS = {d for _k, _d, d, _n in CATEGORIES}
EXPECTED_COUNTS = {d: n for _k, _d, d, n in CATEGORIES}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def corpus_checksum(files: list[Path]) -> str:
    """Path-independent: hash the sorted list of per-file hashes.

    Equivalent to the shell gate::

        find <root> -name '*.md' ! -name '_TEMPLATE.md' -print0 \\
          | xargs -0 shasum -a 256 | awk '{print $1}' | sort | shasum -a 256

    (``-print0``/``-0`` are mandatory: two filenames contain apostrophes.)
    """
    digests = sorted(sha256_file(p) for p in files)
    joined = "".join(f"{d}\n" for d in digests)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def main() -> int:
    root = models_root()
    errors: list[str] = []

    all_md = sorted(root.rglob("*.md"))
    template = root / "_TEMPLATE.md"
    files = [p for p in all_md if p.name != "_TEMPLATE.md"]

    if len(files) != 98:
        errors.append(f"expected 98 model files, found {len(files)}")

    per_dir: dict[str, int] = {}
    seen_slugs: dict[str, str] = {}

    for path in files:
        rel = path.relative_to(root).as_posix()
        parent = path.parent.name
        if parent not in VALID_DIRS:
            errors.append(f"{rel}: parent directory {parent!r} is not one of the 8 categories")
            continue
        per_dir[parent] = per_dir.get(parent, 0) + 1

        if not FILENAME_RE.match(path.name):
            errors.append(f"{rel}: filename does not match m\\d{{2}}_<slug>.md")

        text = path.read_text(encoding="utf-8")

        if len(_NAME.findall(text)) != 1:
            errors.append(f"{rel}: expected exactly one '## Mental Model = <Name>' header")
        if len(_CATEGORY_RAW.findall(text)) != 1:
            errors.append(f"{rel}: expected exactly one '**Category = ...**' line")
        for label, pattern in _LABELS:
            hits = len(pattern.findall(text))
            if hits != 1:
                errors.append(f"{rel}: label for {label!r} matched {hits} times, expected 1")

        parsed = parse_markdown(text)
        for label, _pattern in _LABELS:
            if not parsed[label].strip():
                errors.append(f"{rel}: section {label!r} is empty")
        if not parsed["name"].strip():
            errors.append(f"{rel}: model name is empty")

        slug = path.stem.split("_", 1)[-1] if "_" in path.stem else path.stem
        norm = normalize_slug(slug)
        if norm in seen_slugs:
            errors.append(f"{rel}: normalized slug {norm!r} collides with {seen_slugs[norm]}")
        else:
            seen_slugs[norm] = rel

    for dirname, expected in EXPECTED_COUNTS.items():
        found = per_dir.get(dirname, 0)
        if found != expected:
            errors.append(f"{dirname}: expected {expected} models, found {found}")

    actual = corpus_checksum(files)
    if actual != EXPECTED_CORPUS_SHA256:
        errors.append(
            "CONTENT CHECKSUM MISMATCH -- the model prose was edited, which is "
            f"forbidden.\n  expected {EXPECTED_CORPUS_SHA256}\n  actual   {actual}"
        )
    if template.is_file():
        t = sha256_file(template)
        if t != EXPECTED_TEMPLATE_SHA256:
            errors.append(f"_TEMPLATE.md checksum mismatch: {t}")
    else:
        errors.append("_TEMPLATE.md is missing")

    print(f"content root : {root}")
    print(f"model files  : {len(files)}")
    print(f"checksum     : {actual}")
    if errors:
        print(f"\nFAIL ({len(errors)} problems):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("OK: format, counts, slug uniqueness and checksum all pass.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

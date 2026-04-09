#!/usr/bin/env python3
"""Validate the mental-models skill: frontmatter, model sections, index integrity."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".claude" / "skills" / "mental-models"
SKILL_MD = SKILL_DIR / "SKILL.md"
MODELS_DIR = SKILL_DIR / "models"
INDEX_JSON = SKILL_DIR / "resources" / "model-index.json"

REQUIRED_SECTIONS = [
    "Description",
    "Keywords",
    "Thinking Steps",
    "Coaching Questions",
    "When to Avoid",
]


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip("\n")
    data: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            data[k.strip()] = v.strip()
    return data


def check_skill_md(errors: list[str]) -> None:
    if not SKILL_MD.exists():
        errors.append(f"Missing SKILL.md at {SKILL_MD}")
        return
    text = SKILL_MD.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        errors.append("SKILL.md: missing or malformed YAML frontmatter")
        return
    for field in ("name", "description"):
        if not fm.get(field):
            errors.append(f"SKILL.md: frontmatter missing '{field}'")


def iter_model_files() -> list[Path]:
    files = []
    for p in MODELS_DIR.rglob("*.md"):
        name = p.name
        if name == "_TEMPLATE.md" or name.startswith("_"):
            continue
        files.append(p)
    return sorted(files)


def check_model_file(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8").lower()
    # Models use bold-label convention (**Description:**) rather than H2.
    # Accept either form.
    for required in REQUIRED_SECTIONS:
        needle = required.lower()
        if needle in text:
            continue
        errors.append(
            f"{path.relative_to(REPO_ROOT)}: missing section '{required}'"
        )


def check_index(model_files: list[Path], errors: list[str]) -> None:
    if not INDEX_JSON.exists():
        errors.append(f"Missing index at {INDEX_JSON}")
        return
    try:
        data = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"model-index.json: invalid JSON: {e}")
        return

    indexed_paths: list[str] = []

    def walk(obj):
        if isinstance(obj, dict):
            if "path" in obj and isinstance(obj["path"], str):
                indexed_paths.append(obj["path"])
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    walk(data)

    resolved_indexed: set[Path] = set()
    for rel in indexed_paths:
        abs_path = (SKILL_DIR / rel).resolve()
        if not abs_path.exists():
            errors.append(f"index path does not exist: {rel}")
        else:
            resolved_indexed.add(abs_path)

    on_disk = {p.resolve() for p in model_files}

    missing_from_index = on_disk - resolved_indexed
    for p in sorted(missing_from_index):
        errors.append(
            f"model on disk not referenced in index: {p.relative_to(REPO_ROOT)}"
        )

    stale_in_index = resolved_indexed - on_disk
    for p in sorted(stale_in_index):
        try:
            rel = p.relative_to(REPO_ROOT)
        except ValueError:
            rel = p
        errors.append(f"index references non-model file: {rel}")


def main() -> int:
    errors: list[str] = []
    check_skill_md(errors)

    if not MODELS_DIR.exists():
        errors.append(f"Missing models directory: {MODELS_DIR}")
        model_files: list[Path] = []
    else:
        model_files = iter_model_files()
        for mf in model_files:
            check_model_file(mf, errors)

    check_index(model_files, errors)

    print(f"{len(model_files)} models checked, {len(errors)} errors")
    if errors:
        print("\nFailures:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK: validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Copy the canonical model-index.json into the Python package's bundled data dir.

Run before building or committing the package. CI also runs this and fails on drift.
"""
from __future__ import annotations

import filecmp
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / ".claude" / "skills" / "mental-models" / "resources" / "model-index.json"
DST = REPO / "packages" / "mental_models" / "src" / "mental_models" / "data" / "model-index.json"


def main() -> int:
    if not SRC.is_file():
        print(f"ERROR: source missing: {SRC}", file=sys.stderr)
        return 1
    DST.parent.mkdir(parents=True, exist_ok=True)
    check = "--check" in sys.argv
    if DST.is_file() and filecmp.cmp(SRC, DST, shallow=False):
        print("package data in sync")
        return 0
    if check:
        print("ERROR: package data drift — run `python scripts/sync_package_data.py`", file=sys.stderr)
        return 1
    shutil.copy2(SRC, DST)
    print(f"copied {SRC.relative_to(REPO)} -> {DST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

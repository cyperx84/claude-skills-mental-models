#!/usr/bin/env python3
"""Deterministic selector evals — no LLM, no API key, runs in CI for free.

Tests that `mental_models.select_models(query)` returns expected slugs in the
top-k for a curated set of queries. Catches regressions in the keyword-based
selector when the index or scoring logic changes.

Usage:
    python evals/run_selector_evals.py
    python evals/run_selector_evals.py --cases evals/selector_cases.jsonl
    python evals/run_selector_evals.py --verbose
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_CASES = REPO / "evals" / "selector_cases.jsonl"

# Make the package importable without an install
sys.path.insert(0, str(REPO / "packages" / "mental_models" / "src"))

from mental_models import select_models  # noqa: E402


def load_cases(path: Path) -> list[dict]:
    cases = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            cases.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"error: {path.name}:{i}: {e}", file=sys.stderr)
            sys.exit(3)
    return cases


def run(cases: list[dict], verbose: bool) -> int:
    passed = 0
    failed: list[tuple[str, str, list[str]]] = []
    for case in cases:
        top_k = int(case.get("top_k", 5))
        results = select_models(case["query"], top_k=top_k)
        slugs = [m.slug for m in results]
        expected = case["expect_in_top"]
        missing = [e for e in expected if e not in slugs]
        if missing:
            failed.append((case["id"], case["query"], slugs))
            if verbose:
                print(f"FAIL {case['id']}  q={case['query']!r}")
                print(f"     expected in top-{top_k}: {expected}")
                print(f"     got: {slugs}")
        else:
            passed += 1
            if verbose:
                print(f"PASS {case['id']}  q={case['query']!r}")

    total = len(cases)
    print(f"\n{passed}/{total} selector evals passed")
    if failed:
        print("\nFailures:")
        for cid, q, slugs in failed:
            print(f"  {cid}: {q!r} -> {slugs[:3]}...")
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    if not args.cases.is_file():
        print(f"error: cases file not found: {args.cases}", file=sys.stderr)
        return 3
    cases = load_cases(args.cases)
    return run(cases, args.verbose)


if __name__ == "__main__":
    sys.exit(main())

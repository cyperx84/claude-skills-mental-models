#!/usr/bin/env python3
"""Deterministic evals for the keyword fallback. No LLM, no API key, no network.

Two suites, measuring two different things:

``retrieval_cases.jsonl``
    Exact-name retrieval — query "inversion" expects slug ``inversion``. This is
    the CLI's real job. **100% is required**; anything less fails CI.

``selection_cases.jsonl``
    Natural-language problem statements, graded hit@3. This is the honest
    ledger of where the keyword scorer is wrong. Cases carry a measured
    ``status`` and the runner fails if a ``pass`` regresses **or** if a
    ``known_fail`` starts passing — an improvement is supposed to force a
    ledger update.

Neither suite measures the primary selection path (a harness LLM reading
CATALOG.md), because measuring that needs an API key. See README.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from mental_models_kit import search_models  # noqa: E402

EVALS = REPO / "evals"
RETRIEVAL = EVALS / "retrieval_cases.jsonl"
SELECTION = EVALS / "selection_cases.jsonl"

SELECTION_TOP_K = 3


def load_cases(path: Path) -> list[dict]:
    cases: list[dict] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            cases.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"error: {path.name}:{i}: {e}", file=sys.stderr)
            raise SystemExit(3)
    return cases


def slugs(query: str, k: int) -> list[str]:
    return [m.slug for m in search_models(query, k)]


def run_retrieval(verbose: bool) -> tuple[int, int, list[str]]:
    cases = load_cases(RETRIEVAL)
    failures: list[str] = []
    passed = 0
    print("retrieval — exact-name lookup (must be 100%)")
    for case in cases:
        k = int(case.get("top_k", 5))
        got = slugs(case["query"], k)
        want = list(case["expect_in_top"])
        ok = all(w in got for w in want)
        passed += ok
        mark = "PASS" if ok else "FAIL"
        if not ok:
            failures.append(f"{case['id']}: {case['query']!r} -> {got} (wanted {want})")
        if verbose or not ok:
            print(f"  {mark}  {case['id']:<8} {case['query']!r} -> {got}")
    print(f"  {passed}/{len(cases)}")
    return passed, len(cases), failures


def run_selection(verbose: bool) -> tuple[int, int, int, list[str]]:
    cases = load_cases(SELECTION)
    failures: list[str] = []
    hit3 = 0
    hit1 = 0
    known_fail = 0
    print(f"\nselection — natural-language problems, hit@{SELECTION_TOP_K}")
    for case in cases:
        want = set(case["expect_any_of"])
        got = slugs(case["query"], SELECTION_TOP_K)
        ok3 = bool(want & set(got))
        ok1 = bool(want & set(got[:1]))
        hit3 += ok3
        hit1 += ok1
        status = case.get("status", "known_fail")
        known_fail += status == "known_fail"
        mark = "hit " if ok3 else "miss"
        if verbose:
            print(f"  {mark} [{status:<10}] {case['id']:<8} {case['query']!r} -> {got}")
            stale = case.get("observed_top3")
            if stale is not None and stale != got:
                print(f"       ledger note: observed_top3 recorded as {stale}")
        if status == "pass" and not ok3:
            failures.append(
                f"{case['id']} regressed: status \"pass\" but hit@{SELECTION_TOP_K} missed. "
                f"got {got}, wanted any of {sorted(want)}"
            )
        if status == "known_fail" and ok3:
            failures.append(
                f"known-fail case {case['id']} now passes — promote it to "
                'status:"pass" and commit the ledger'
            )
    print(f"  hit@1 {hit1}/{len(cases)} · hit@{SELECTION_TOP_K} {hit3}/{len(cases)}")
    return hit3, len(cases), known_fail, failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-v", "--verbose", action="store_true", help="Print every case")
    args = ap.parse_args()

    r_pass, r_total, r_fail = run_retrieval(args.verbose)
    s_pass, s_total, s_known, s_fail = run_selection(args.verbose)

    if r_pass != r_total:
        r_fail.append(f"retrieval must be {r_total}/{r_total}, got {r_pass}")

    print(
        f"\nsummary: retrieval {r_pass}/{r_total} · "
        f"selection {s_pass}/{s_total} ({s_known} known_fail)"
    )
    problems = r_fail + s_fail
    if problems:
        print("\nFAIL:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Regression eval harness for the mental-models skill.

Pipeline: generator -> judge -> aggregator

- Generator: invokes Claude (via Anthropic SDK, or `claude` CLI fallback) on
  each prompt in cases.jsonl.
- Judge: an LLM-judge (see `judge.py`) grades each response against a rubric
  (model_selection, reasoning_quality, actionability; 0-2 each, total 0-6,
  pass >= 4). Substring mode is retained as a legacy fallback.
- Aggregator: prints a per-case table, overall pass rate, mean score, and
  pass rate by category; optionally writes full results to a JSONL file.

Exit code: 0 if pass rate >= 0.7, else 1.

Usage
-----
    python3 evals/run_evals.py --dry-run
    python3 evals/run_evals.py                       # judge mode, default
    python3 evals/run_evals.py --mode substring      # legacy substring match
    python3 evals/run_evals.py --out evals/baselines/$(date +%Y-%m-%d).jsonl

Requires `pip install anthropic` and `ANTHROPIC_API_KEY` for judge mode (and
for SDK-based generation). Substring mode can still use the `claude` CLI.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import statistics
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

CASES_PATH = Path(__file__).parent / "cases.jsonl"
REQUIRED_FIELDS = {"id", "prompt", "expected_models", "category"}
DEFAULT_MODEL = "claude-opus-4-6"
PASS_RATE_THRESHOLD = 0.7


def load_cases(path: Path) -> list[dict]:
    cases: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise SystemExit(f"{path}:{lineno}: invalid JSON - {e}")
            missing = REQUIRED_FIELDS - obj.keys()
            if missing:
                raise SystemExit(
                    f"{path}:{lineno}: missing fields {sorted(missing)}"
                )
            if not isinstance(obj["expected_models"], list) or not obj["expected_models"]:
                raise SystemExit(
                    f"{path}:{lineno}: expected_models must be a non-empty list"
                )
            cases.append(obj)
    return cases


def normalize(text: str) -> str:
    return text.lower().replace("_", " ").replace("-", " ")


# ---------- generation ----------

def generate_sdk(prompt: str, model: str) -> str:
    try:
        import anthropic  # type: ignore
    except ImportError:
        print(
            "error: `anthropic` package not installed. Run `pip install anthropic`.",
            file=sys.stderr,
        )
        sys.exit(2)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("error: ANTHROPIC_API_KEY not set.", file=sys.stderr)
        sys.exit(2)
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    parts = []
    for block in msg.content:
        if getattr(block, "type", None) == "text":
            parts.append(block.text)
    return "\n".join(parts)


def generate_cli(prompt: str, timeout: int = 180) -> str:
    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        raise SystemExit("error: `claude` CLI not found.")
    except subprocess.TimeoutExpired:
        return ""
    return (result.stdout or "") + "\n" + (result.stderr or "")


def generate(prompt: str, model: str) -> str:
    # Prefer SDK path when available; fall back to CLI.
    try:
        import anthropic  # noqa: F401
        if os.environ.get("ANTHROPIC_API_KEY"):
            return generate_sdk(prompt, model)
    except ImportError:
        pass
    if shutil.which("claude"):
        return generate_cli(prompt)
    print(
        "error: neither `anthropic` SDK (with ANTHROPIC_API_KEY) nor `claude` CLI available.",
        file=sys.stderr,
    )
    sys.exit(2)


# ---------- grading ----------

def grade_substring(case: dict, response: str) -> dict:
    haystack = normalize(response)
    hits = [s for s in case["expected_models"] if normalize(s) in haystack]
    passed = len(hits) > 0
    # Map to rubric-shaped record for unified output.
    score = 2 * len(hits) // max(1, len(case["expected_models"]))
    return {
        "mode": "substring",
        "hits": hits,
        "scores": {"substring_hits": len(hits)},
        "total": len(hits),
        "pass": passed,
        "rationale": f"substring hits: {hits}",
    }


def grade_judge(case: dict, response: str, judge_model: str) -> dict:
    from judge import judge_response  # local import so --dry-run doesn't need it

    r = judge_response(case, response, model=judge_model)
    return {
        "mode": "judge",
        "scores": r.scores,
        "total": r.total,
        "pass": r.pass_,
        "rationale": r.rationale,
    }


# ---------- output ----------

def print_table(rows: list[list[str]]) -> None:
    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    sep = "  "
    for i, row in enumerate(rows):
        print(sep.join(cell.ljust(widths[j]) for j, cell in enumerate(row)))
        if i == 0:
            print(sep.join("-" * w for w in widths))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="validate cases.jsonl without invoking any model")
    parser.add_argument("--mode", choices=["substring", "judge"], default="judge")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="generator model id")
    parser.add_argument("--judge-model", default=DEFAULT_MODEL,
                        help="judge model id (same-model grading is v1 default)")
    parser.add_argument("--cases", type=Path, default=CASES_PATH)
    parser.add_argument("--out", type=Path, default=None,
                        help="write full results as JSONL")
    args = parser.parse_args()

    cases = load_cases(args.cases)
    print(f"loaded {len(cases)} cases from {args.cases}")

    if args.dry_run:
        print("dry-run ok")
        return 0

    print(f"mode={args.mode} generator={args.model} judge={args.judge_model}")

    results: list[dict] = []
    rows: list[list[str]] = [["id", "category", "result", "score", "notes"]]

    for case in cases:
        response = generate(case["prompt"], args.model)
        if args.mode == "judge":
            graded = grade_judge(case, response, args.judge_model)
            notes = graded["rationale"][:60].replace("\n", " ")
            score_str = f"{graded['total']}/6"
        else:
            graded = grade_substring(case, response)
            notes = ",".join(graded["hits"]) or "-"
            score_str = str(graded["total"])

        record = {
            "id": case["id"],
            "category": case["category"],
            "prompt": case["prompt"],
            "expected_models": case["expected_models"],
            "response": response,
            **graded,
        }
        results.append(record)
        rows.append([
            case["id"],
            case["category"],
            "PASS" if graded["pass"] else "FAIL",
            score_str,
            notes,
        ])

    print()
    print_table(rows)
    print()

    passes = sum(1 for r in results if r["pass"])
    pass_rate = passes / len(results) if results else 0.0
    mean_score = statistics.mean(r["total"] for r in results) if results else 0.0
    print(f"pass rate: {passes}/{len(results)} = {pass_rate:.0%}")
    print(f"mean score: {mean_score:.2f}")

    by_cat: dict[str, list[bool]] = defaultdict(list)
    for r in results:
        by_cat[r["category"]].append(r["pass"])
    print("by category:")
    for cat, vals in sorted(by_cat.items()):
        p = sum(vals) / len(vals)
        print(f"  {cat}: {sum(vals)}/{len(vals)} ({p:.0%})")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8") as f:
            for r in results:
                f.write(json.dumps(r) + "\n")
        print(f"wrote {args.out}")

    return 0 if pass_rate >= PASS_RATE_THRESHOLD else 1


if __name__ == "__main__":
    sys.exit(main())

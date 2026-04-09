#!/usr/bin/env python3
"""Regression eval harness for the mental-models skill.

Reads cases from cases.jsonl, invokes the Claude Code CLI in non-interactive
mode for each prompt, and checks whether the response mentions the expected
model slugs via case-insensitive substring matching.

LIMITATIONS
-----------
- Matching is approximate. Substring matches on slugs will miss responses that
  discuss a model without naming it (e.g. talks about "working backwards from
  failure" without writing the word "inversion").
- Slug underscores/hyphens are normalized to spaces before matching, so
  "second-order_thinking" matches "second order thinking" in prose.
- Activation and selection quality are not separated: if the skill fails to
  load at all, every case will fail.
- Results depend on the Claude model version behind the CLI. Record it when
  investigating regressions.
- Requires the Claude Code CLI (`claude`) to be installed and authenticated.
  See https://docs.claude.com/en/docs/claude-code/overview

Usage
-----
    python3 evals/run_evals.py              # full run
    python3 evals/run_evals.py --dry-run    # validate cases.jsonl only
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

CASES_PATH = Path(__file__).parent / "cases.jsonl"
REQUIRED_FIELDS = {"id", "prompt", "expected_models", "category"}


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


def run_claude(prompt: str, timeout: int = 180) -> str:
    # Requires Claude Code CLI installed: `claude -p` runs a one-shot prompt.
    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        raise SystemExit(
            "error: `claude` CLI not found. Install Claude Code and try again."
        )
    except subprocess.TimeoutExpired:
        return ""
    return (result.stdout or "") + "\n" + (result.stderr or "")


def evaluate(case: dict, response: str) -> tuple[bool, list[str]]:
    haystack = normalize(response)
    hits = []
    for slug in case["expected_models"]:
        if normalize(slug) in haystack:
            hits.append(slug)
    # Pass criterion: at least one expected model surfaces.
    return (len(hits) > 0, hits)


def print_table(rows: list[tuple[str, str, str, str]]) -> None:
    widths = [max(len(r[i]) for r in rows) for i in range(4)]
    sep = "  "
    for i, row in enumerate(rows):
        line = sep.join(cell.ljust(widths[j]) for j, cell in enumerate(row))
        print(line)
        if i == 0:
            print(sep.join("-" * w for w in widths))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate cases.jsonl without invoking the CLI",
    )
    parser.add_argument(
        "--cases",
        type=Path,
        default=CASES_PATH,
        help="path to cases.jsonl",
    )
    args = parser.parse_args()

    cases = load_cases(args.cases)
    print(f"loaded {len(cases)} cases from {args.cases}")

    if args.dry_run:
        print("dry-run ok")
        return 0

    rows: list[tuple[str, str, str, str]] = [
        ("id", "category", "result", "hits"),
    ]
    failures = 0
    for case in cases:
        response = run_claude(case["prompt"])
        passed, hits = evaluate(case, response)
        if not passed:
            failures += 1
        rows.append(
            (
                case["id"],
                case["category"],
                "PASS" if passed else "FAIL",
                ",".join(hits) if hits else "-",
            )
        )

    print()
    print_table(rows)
    print()
    print(f"{len(cases) - failures}/{len(cases)} passed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

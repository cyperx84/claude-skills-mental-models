# Evals

Lightweight regression harness for the `mental-models` skill.

## Purpose

Changes to `SKILL.md` (description, trigger phrases, progressive disclosure layout)
can silently degrade two things:

1. **Activation** - whether the model decides to load the skill at all.
2. **Selection quality** - whether, once loaded, the model picks sensible mental
   models for the user's problem.

This harness exists so we can notice regressions before shipping them. It is not a
benchmark - it is a smoke test.

## How it works

- `cases.jsonl` - one eval case per line. Each case has a prompt and a set of
  `expected_models` (slugs from `.claude/skills/mental-models/resources/model-index.json`)
  that a well-functioning skill should surface.
- `run_evals.py` - runs each prompt through the `claude` CLI in non-interactive mode
  (`claude -p`), captures the response, and does a substring match against the
  expected model slugs. Prints a pass/fail table and exits non-zero on failure.

Matching is deliberately loose (case-insensitive substring). We care about "did the
model name show up" not "was the response word-perfect".

## Running

Prerequisites:
- Python 3.9+
- Claude Code CLI installed and authenticated (`claude --version` should work)

```
# Validate the case file without invoking the CLI
python3 evals/run_evals.py --dry-run

# Full run
python3 evals/run_evals.py
```

Exit code is `0` if every case passes, `1` otherwise.

## Adding cases

1. Append a JSON object to `cases.jsonl` (one per line, no trailing comma).
2. Use an `id` like `eval-016`.
3. Pick 1-3 `expected_models` that a thoughtful human applying Munger's latticework
   would reach for. Use the exact slug from `model-index.json`.
4. Run `python3 evals/run_evals.py --dry-run` to confirm the file parses.

## Limitations

- Substring matching is approximate - a response that discusses inversion without
  using the word "inversion" will be marked as failing.
- Activation is not isolated from selection; if the skill fails to load, every case
  fails.
- Results are model-version dependent. Record the Claude model ID when investigating
  regressions.

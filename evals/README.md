# Evals

Regression harness for the `mental-models` skill.

## Architecture

```
cases.jsonl  ->  generator  ->  judge  ->  aggregator
                 (Claude)      (LLM)      (table + stats)
```

- **Generator** (`run_evals.py`): runs each prompt in `cases.jsonl` through
  Claude. Prefers the Anthropic SDK (`pip install anthropic`) and falls back
  to the `claude` CLI when the SDK or API key is unavailable.
- **Judge** (`judge.py`): an LLM-judge that grades each response against a
  3-criterion rubric using structured tool-use output.
- **Aggregator**: prints a per-case table plus overall pass rate, mean score,
  and pass rate by category; optionally writes a JSONL results file.

## Rubric

Each criterion is scored 0-2 (max total 6, pass threshold 4):

| Criterion           | 0                           | 1                                    | 2                                           |
|---------------------|-----------------------------|--------------------------------------|---------------------------------------------|
| `model_selection`   | None of the expected models | One relevant model or just names     | Two+ expected (or defensible) with substance |
| `reasoning_quality` | Name-drops only             | Walks reasoning for one model        | Walks thinking for multiple models          |
| `actionability`     | Vague / abstract            | Some concrete + some vague           | Clear concrete next steps                   |

A case passes when `total >= 4`. The run passes when pass rate >= 70%.

## Running

Prerequisites:

- Python 3.9+
- `pip install anthropic` (see `[dev]` note below)
- `ANTHROPIC_API_KEY` exported in the environment
- Or, for substring mode only, the `claude` CLI

```bash
# Validate cases file only (no API calls)
python3 evals/run_evals.py --dry-run

# Full judge run (default)
python3 evals/run_evals.py

# Legacy substring mode
python3 evals/run_evals.py --mode substring

# Write full results to a baseline snapshot
python3 evals/run_evals.py --out evals/baselines/$(date +%Y-%m-%d).jsonl

# Override generator or judge model
python3 evals/run_evals.py --model claude-opus-4-6 --judge-model claude-opus-4-6
```

Exit code is `0` if pass rate >= 0.7, else `1`.

## Adding cases

1. Append a JSON object to `cases.jsonl` (one per line).
2. Use an `id` like `eval-016`.
3. Pick 1-3 `expected_models` a thoughtful human would reach for. Use the
   exact slug from `.claude/skills/mental-models/resources/model-index.json`.
4. Run `python3 evals/run_evals.py --dry-run` to confirm it parses.

## Known limitations

- **Same-model grading bias**: v1 uses the same model family for generator
  and judge. This is cheap and simple but inflates scores. Plan to add
  cross-model grading in a future iteration.
- **Rubric subjectivity**: expect +/- 1 point per criterion between repeat
  runs. Small deltas are noise.
- **Cost**: ~15 cases * 2 calls (generate + judge) ~= 30 requests per run.
  At Opus pricing this is roughly a few cents to low dollars per run,
  depending on response length.
- **Activation vs. selection**: if the skill fails to load entirely, every
  case fails and the rubric can't disambiguate why.

## `[dev]` dependency note

Eval running requires the Anthropic SDK and an API key:

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

These are **not** required to develop the skill itself, only to run the
harness. They are intentionally not in any hard dependency list.

## CI

Evals are **not** wired into CI by default (API key + cost). A manual
workflow `.github/workflows/evals.yml` is provided - trigger it via
workflow_dispatch. It requires an `ANTHROPIC_API_KEY` repository secret
and uploads the results JSONL as an artifact.

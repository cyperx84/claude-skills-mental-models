# Baselines

Snapshots of full eval runs. Useful for comparing skill changes against a
known reference point.

## v0.2.0 baseline (pending)

The v0.2.0 baseline has not been captured yet because `ANTHROPIC_API_KEY` was
not available in the environment at the time this stub was written (2026-04-09).

Once the key is exported, run the following command to capture it:

```bash
export ANTHROPIC_API_KEY=sk-ant-...

# Capture first 10 cases against the pinned mid-tier model
head -n 10 evals/cases.jsonl > /tmp/cases-10.jsonl
python3 evals/run_evals.py \
  --cases /tmp/cases-10.jsonl \
  --model claude-sonnet-4-6 \
  --judge-model claude-sonnet-4-6 \
  --out evals/baselines/v0.2.0-sonnet-4-6.jsonl
```

Then update this file with:
- Model: `claude-sonnet-4-6`
- Date: (date of run)
- Case count: 10
- Pass rate and mean score from the harness output

Commit the `.jsonl` file and this README together on `feat/polish-next-steps`.

## Capture a full snapshot

```bash
python3 evals/run_evals.py --out evals/baselines/$(date +%Y-%m-%d).jsonl
```

Each line in the output is a full result record: `id`, `category`, `prompt`,
`expected_models`, `response`, `scores`, `total`, `pass`, `rationale`.

## Comparing

A diff between two baselines tells you whether a change to `SKILL.md` moved
scores up or down. Treat small deltas (+/- 1 per criterion) as noise.

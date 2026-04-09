# Baselines

Snapshots of full eval runs. Useful for comparing skill changes against a
known reference point.

## Capture a snapshot

```bash
python evals/run_evals.py --out evals/baselines/$(date +%Y-%m-%d).jsonl
```

Each line in the output is a full result record: `id`, `category`, `prompt`,
`expected_models`, `response`, `scores`, `total`, `pass`, `rationale`.

## Comparing

A diff between two baselines tells you whether a change to `SKILL.md` moved
scores up or down. Treat small deltas (+/- 1 per criterion) as noise.

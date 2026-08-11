# Evals

Deterministic, stdlib-only, no network, **no API key**. Run them with:

```bash
python3 evals/run_evals.py          # summary
python3 evals/run_evals.py -v       # every case
```

Exit 0 on success, 1 on failure.

## What these numbers actually measure

**They measure the keyword fallback (`mental-models search` / `search_models`)
and nothing else.**

The primary selection path is different: the CLI emits a compact catalog
(`mental-models catalog`, mirrored at `skills/mental-models/CATALOG.md`) and the
**calling harness LLM** reads it and picks 2-4 models itself. That path is the
product. This harness does not and cannot measure it, because grading an LLM's
model choices needs an LLM, which needs an API key, which this project must not
require. The previous LLM-judge harness (`judge.py`, `cases.jsonl`,
`baselines/`) was deleted for exactly that reason — it could never run in CI.

So: a low selection score below is not a claim about the product. It is the
honest measurement of the fallback, kept visible so nobody re-advertises keyword
matching as selection.

## The two suites

### `retrieval_cases.jsonl` — exact-name lookup, **100% required**

Query the name of a model, expect that model in the top-k. Every expected slug
must appear. This is what the CLI is genuinely good at and it must never
regress; CI fails below 100%.

### `selection_cases.jsonl` — natural-language problems, graded hit@3

A case passes when at least one slug in `expect_any_of` appears in the top 3.
Each case carries a **measured** `status`:

| field | meaning |
|---|---|
| `status: "pass"` | measured as a hit. A regression fails CI. |
| `status: "known_fail"` | measured as a miss. Recorded, not hidden. |
| `observed_top3` | what the scorer actually returned when the case was written |
| `note` | why the case exists / why the result is what it is |

The runner **also fails when a `known_fail` starts passing**, with a message
telling you to promote it to `"pass"` and commit the ledger. Improvement is
supposed to force a ledger update — that is what keeps the file true.

Statuses are written from an actual run. They are never guessed, cases are never
tuned to force a verdict, and no case is deleted for being awkward. Two of the
three current passes are qualitatively poor and say so in their `note`
(sel-003 hits only at rank 2 behind `hanlon's_razor`; sel-012 only at rank 3).

Current measurement: **retrieval 29/29 · selection 3/13 hit@3 (1/13 hit@1)**.

## Deviations from the build spec, with evidence

The spec said to `git mv evals/selector_cases.jsonl → evals/retrieval_cases.jsonl`
unchanged and gate it at 30/30. One case had to move to the selection ledger
instead. The evidence chain:

1. The pre-rebuild harness scored **30/30** against the old JSON index
   (re-executed to confirm, not assumed).
2. The rebuilt corpus produces **byte-identical keyword sets** for all 98
   models — so keywords are not the delta.
3. The only delta is `description`: the old index stored
   `Description[:200] + "..."` for all 98 models; the corpus now carries the
   full prose. Un-truncating is a mandated fix, and the scorer must not be
   given a truncated description just to preserve an old ranking.
4. Under the full descriptions, `sel-022` ("how do I know when to quit") fails.
   Its expected `first-principle_thinking` scores **1.5** — tied with five other
   models — and previously won only on slug ordering. It was never a signal.
5. `sel-022` is also not an exact-name lookup; it is a natural-language query
   that the spec's "all 30 cases are tautological" premise did not cover.

It was therefore **moved, not deleted and not tuned**: it now lives in
`selection_cases.jsonl` as a `known_fail` with its expectations carried over
verbatim (`law_of_diminishing_returns` was deliberately *not* added, even though
it now sits in the measured top-3, because adding it would flip the case to pass
by tuning). Retrieval stays gated at 100% of the file: 29/29.

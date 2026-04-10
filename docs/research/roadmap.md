# Roadmap: backlog from the landscape review

Six backlog items extracted from [`landscape.md`](./landscape.md), formatted so each section can be pasted into a GitHub issue as-is. ROI-ordered.

---

## 1. `feat: \`walk <slug>\` subcommand — stepwise thinking-steps iterator`

**Problem.** `mental-models apply <slug>` returns the full `thinking_steps` block at once. For reasoning-heavy problems, the user wants to step through the framework one beat at a time, revise an earlier step when new information surfaces, or branch to an alternative approach — the pattern popularized by the [sequentialthinking MCP server](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking).

**Proposed approach.**
- New CLI subcommand `mental-models walk <slug> [--problem "..."]` in `packages/mental_models/src/mental_models/cli.py`.
- Parse the existing `thinking_steps` block (already extracted by `_extract_sections`, `cli.py:247`) into a list of steps — split on leading numbered markers (`^\s*\d+[.)]\s+`).
- Interactive loop: `next` advances, `revise` replaces the current step's output, `branch` forks to a sibling model, `done` exits. JSON mode emits one NDJSON record per action.
- Mirror as `mm_walk` in `packages/mental_models_mcp/src/mental_models_mcp/server.py`.
- Add an env-var escape hatch `MENTAL_MODELS_DISABLE_WALK_LOGGING` echoing sequentialthinking's `DISABLE_THOUGHT_LOGGING`.

**Files touched.**
- `packages/mental_models/src/mental_models/cli.py` — new `cmd_walk`, argparse subparser.
- `packages/mental_models/src/mental_models/selector.py` — no change.
- `packages/mental_models_mcp/src/mental_models_mcp/server.py` — new `mm_walk` tool.
- `packages/mental_models/tests/` — unit test for the step-splitter regex against 3 sample models.

**Acceptance criteria.**
- `mental-models walk inversion` steps through inversion's thinking steps one at a time, and `--json` emits NDJSON.
- `mm_walk` is listed by `mm_doctor` and callable from Claude Desktop.
- The step splitter handles all 98 models without raising (smoke test).

**Labels.** `enhancement`, `cli`, `mcp`

---

## 2. `feat: \`select --clarify\` flag — scoping questions before model selection`

**Problem.** Selector quality is bounded by how narrow the user's query is. A 5-word query like "scaling issues" matches dozens of models weakly. Asking 2–3 scoping questions first — inspired by [nidhinjs/prompt-master](https://github.com/nidhinjs/prompt-master) — lets the user enrich the query before the selector runs.

**Proposed approach.**
- Add `--clarify` flag to `cmd_select` in `packages/mental_models/src/mental_models/cli.py`.
- New helper `suggest_clarifying_questions(query: str) -> list[str]` in `packages/mental_models/src/mental_models/selector.py`. Keyword-driven, not LLM-driven: match query tokens against a small taxonomy (decision / diagnosis / planning / critique) and emit the canonical questions for the matched class.
- With `--clarify`, the CLI prints the questions and exits 0; the user re-runs `select` with the enriched query.
- JSON mode emits `{"query": ..., "clarifying_questions": [...]}`.

**Files touched.**
- `packages/mental_models/src/mental_models/cli.py` — flag, handler branch.
- `packages/mental_models/src/mental_models/selector.py` — `suggest_clarifying_questions` + a tiny question taxonomy.
- `packages/mental_models/tests/` — unit test on the taxonomy mapping.

**Acceptance criteria.**
- `mental-models select "scaling issues" --clarify` prints 2–3 questions.
- `--json` output is stable across identical queries (deterministic).
- No new runtime dependencies.

**Labels.** `enhancement`, `cli`

---

## 3. `feat: intent-router pre-classifier for the keyword selector`

**Problem.** The current keyword selector in `packages/mental_models/src/mental_models/selector.py:57` scores each model independently, so queries with overlapping tokens can surface unrelated models. An intent-router — inspired by [ckelsoe/claude-skill-prompt-architect](https://github.com/ckelsoe/claude-skill-prompt-architect) — classifies the query into one of a small set of intent classes (`decision` / `diagnosis` / `planning` / `critique`) and biases the score toward the model cluster associated with that intent.

**Proposed approach.**
- New `_classify_intent(query_tokens: list[str]) -> str | None` in `selector.py`. Keyword-driven, matches a small static map; returns `None` when unsure.
- In `_score`, add a small boost when a model's category or keywords align with the detected intent class.
- Static intent → model-cluster map lives in a new constant at the top of `selector.py`; no file I/O.
- New regression cases in `evals/selector_cases.jsonl` exercising the intent boost on ambiguous queries.

**Files touched.**
- `packages/mental_models/src/mental_models/selector.py` — new function, score boost.
- `evals/selector_cases.jsonl` — ~5 new cases.

**Acceptance criteria.**
- `python evals/run_selector_evals.py` stays at 30/30 + new cases.
- At least 3 previously-low-ranked "obvious" models now surface in the top-5 for their matching intent class (documented in the PR description).

**Labels.** `enhancement`, `selector`

---

## 4. `docs: GitHub Pages catalog site`

**Problem.** `docs/categories.md`, `docs/latticework.svg`, and `docs/latticework.json` already exist but aren't browsable on the web. A Pages site is a high-leverage discoverability win for the project, no content work required.

**Proposed approach.**
- New workflow `.github/workflows/pages.yml` that deploys `docs/` to GitHub Pages on every push to `main`.
- New `docs/index.md` landing page linking to the categories, the rendered latticework, and `docs/research/landscape.md`.
- Enable Pages in repo Settings (manual step).

**Files touched.**
- `.github/workflows/pages.yml` (new).
- `docs/index.md` (new, ~40 lines).

**Acceptance criteria.**
- Pushing to `main` deploys a live Pages site.
- The latticework SVG renders.
- Category and model pages are reachable within 2 clicks.

**Labels.** `docs`, `ci`

---

## 5. `chore: gap audit vs. 129-model list from sourcesofinsight`

**Problem.** We ship 98 models; [sourcesofinsight.com](https://sourcesofinsight.com/charlie-munger-mental-models/) curates a 129-entry list from Munger's talks. Worth closing the gap where the extras pass our curation bar (distinct model, not a restatement, has clear thinking steps).

**Proposed approach.**
- Extract the 129-entry list into a scratch file.
- Diff against `docs/categories.md` to identify missing models.
- For each new model that passes curation: author a `models/Mental_Model_<Category>/m<NN>_<name>.md` file following `_TEMPLATE.md`, rebuild `resources/model-index.json`, regenerate `docs/latticework.json` + SVG.

**Files touched.**
- `.claude/skills/mental-models/models/` — new files.
- `.claude/skills/mental-models/resources/model-index.json` — regenerated.
- `docs/latticework.json`, `docs/latticework.svg` — regenerated.
- `docs/categories.md` — counts updated.

**Acceptance criteria.**
- Selector evals still 30/30.
- New models appear in `mental-models list`.
- PR description lists each added model with a one-line rationale.

**Labels.** `content`

---

## 6. `chore: submit skill to awesome-agent-skills and awesome-claude-skills`

**Problem.** Free distribution via two curated lists — no local code change, just two upstream PRs.

**Proposed approach.**
- Open a PR on [`VoltAgent/awesome-agent-skills`](https://github.com/VoltAgent/awesome-agent-skills) adding `mental-models` in the reasoning/decision-making section.
- Open a PR on [`ComposioHQ/awesome-claude-skills`](https://github.com/ComposioHQ/awesome-claude-skills) in the matching section.
- Use the short description and link to the rendered README.

**Files touched.** None in this repo.

**Acceptance criteria.**
- Both upstream PRs merged (or at least open + linked here).

**Labels.** `distribution`

---

## Notes

- This file exists because the GitHub MCP tools weren't available in the session where the landscape research landed. Items here should be turned into real GitHub issues when someone next has write access — each H2 is shaped so the body below it pastes cleanly into an issue body.
- Items 5 and 6 are parallel-safe with any of 1–4.
- Item 3 (intent-router) should land after item 2 (--clarify) if both are in flight, so the intent taxonomy has a single home.

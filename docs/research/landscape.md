# Landscape research: similar projects + repo naming

_Last updated: 2026-04-10. Companion to the 0.2.0 release._

## Purpose

Two questions prompted this doc:

1. **What can we learn from comparable projects** in the mental-models, structured-reasoning, and Claude-skills space? Specifically: which features are worth porting back into this repo?
2. **Is `claude-skills-mental-models` the right repository name**, given that the project now ships a CLI, Python library, MCP server, and a portable AgentSkills variant — not just a Claude Code skill?

The answers shape a small backlog of feature issues (see bottom of this doc) and a rename recommendation.

---

## Part 1 — Similar projects worth learning from

### A. Direct content analogues (mental-model catalogs)

| Project | What it is | What's worth stealing |
|---|---|---|
| [ModelThinkers](https://modelthinkers.com/mental-model/mungers-latticework) | Web app, ~200 models, user-built "latticeworks", spaced repetition | A `model-of-the-day` CLI command and user-saved latticeworks (`mental-models save-lattice "pricing"`). Retention hook, low leverage until there's usage data. |
| [WiseCharlie/mental-models](https://github.com/WiseCharlie/mental-models) | Static content collection | Cross-check our 98 against their list for gaps; borrow phrasings and citations where ours are thinner. |
| [AdrienLemaire/awesome-mental-models](https://github.com/AdrienLemaire/awesome-mental-models) | Awesome-list of heuristics and tools-for-thought | Mine for missing models (intuition pumps, atomic-habits framings). |
| [mahavak.github.io/models](https://mahavak.github.io/models/) | Static site rendering of Munger's framework | Publish a GitHub Pages site from `docs/` — our `docs/latticework.svg`, `docs/latticework.json`, and `docs/categories.md` already cover the content. Pages is a thin workflow wrap. |
| [sourcesofinsight — 129 list](https://sourcesofinsight.com/charlie-munger-mental-models/) | Curated 129-model list | Gap-analysis target. We ship 98; they list 129. Worth an audit to close the gap where the extra models pass our curation bar. |

### B. Structural / behavioral analogues (reasoning skills and MCP servers)

| Project | Pattern to borrow |
|---|---|
| [modelcontextprotocol/servers — sequentialthinking](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) | **Stepwise thought protocol**: their tool emits `thought`, `revision`, `branch`, `hypothesis` nodes. We can add a `walk <slug>` command that iterates an existing model's `thinking_steps` one step at a time, allowing revision and branching. This is an increment on existing plumbing — `cmd_apply` in [`packages/mental_models/src/mental_models/cli.py`](../../packages/mental_models/src/mental_models/cli.py) already parses `thinking_steps` via `_extract_sections`, so `walk` only needs a step-splitter and an interactive loop. Their `DISABLE_THOUGHT_LOGGING` env-var is a nice ergonomic touch to copy. |
| [mettamatt/code-reasoning](https://github.com/mettamatt/code-reasoning) | Fork of sequential-thinking specialized for code. Demonstrates the "specialize a generic reasoning server for a domain" pattern. We could ship `mental-models-code`, `mental-models-product`, etc. as thin presets — but wait until we have usage data. |
| [ckelsoe/claude-skill-prompt-architect](https://github.com/ckelsoe/claude-skill-prompt-architect) | 7 prompt frameworks (CO-STAR, RISEN, RTF, CoT…) with an **intent-router** that picks the right framework from the user's phrasing. Our selector already keyword-routes; we can upgrade it to an intent taxonomy (`decision` / `diagnosis` / `planning` / `critique`) and bias the score toward the matching model cluster. This is a `_score` refinement in [`packages/mental_models/src/mental_models/selector.py`](../../packages/mental_models/src/mental_models/selector.py), not a rewrite, and it's already covered by the regression cases in [`evals/selector_cases.jsonl`](../../evals/selector_cases.jsonl). |
| [nidhinjs/prompt-master](https://github.com/nidhinjs/prompt-master) | Extracts 9 "intent dimensions" (task, constraints, audience, success criteria…) before answering. Worth stealing: a `select --clarify` flag that asks 2–3 scoping questions before model selection, so the lattice is chosen against a richer problem statement. Small CLI surface change, no index impact. |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 1000+ skills index — free distribution once we submit. |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | Same — submit. |
| [glebis/claude-skills](https://github.com/glebis/claude-skills) | Collection showing common skill-repo conventions; sanity-check our structure against it. |

### C. Feature shortlist (ROI-ordered)

Each row names the repo file that would change when the feature ships. Full issue-shaped bodies live in [`docs/research/roadmap.md`](./roadmap.md); copy an H2 from there into a new GitHub issue when ready.

| # | Feature | Source of idea | Files touched | Blast radius |
|---|---|---|---|---|
| 1 | `walk <slug>` subcommand — iterate parsed `thinking_steps` with `next` / `revise` / `branch` / `done` actions | modelcontextprotocol sequentialthinking | `packages/mental_models/src/mental_models/cli.py` (new `cmd_walk`), mirror tool in `packages/mental_models_mcp/src/mental_models_mcp/server.py` | Small — reuses `_extract_sections`; adds a step-splitter regex |
| 2 | `select --clarify` flag — emit 2–3 scoping questions before returning models | prompt-master | `cli.py` `cmd_select` (add flag), `selector.py` (new `suggest_clarifying_questions`) | Small — pure text, no index change |
| 3 | Intent-router pre-classifier — map query → intent class → bias model cluster | prompt-architect | `selector.py` `_score` (add intent boost), new `_classify_intent`; regression cases in `evals/selector_cases.jsonl` | Medium — touches scoring; evals guard it |
| 4 | GitHub Pages catalog site | mahavak.github.io/models | new `.github/workflows/pages.yml`, new `docs/index.md`; wraps existing `docs/latticework.svg` and `docs/categories.md` | Small — docs only |
| 5 | Gap audit vs. 129-list (sourcesofinsight) | sourcesofinsight.com | new model files under `.claude/skills/mental-models/models/`, index rebuild | Medium — content curation |
| 6 | Submit skill to `VoltAgent/awesome-agent-skills` + `ComposioHQ/awesome-claude-skills` | those repos | upstream PRs, no local change | Zero |

**Explicitly deferred**:

- **`model-of-the-day` / spaced repetition** (ModelThinkers) — fun but low leverage until there's meaningful usage data.
- **Domain presets** (`mental-models-code`, `-product`, …) (mettamatt) — premature. Wait until usage shows a real domain split.

---

## Part 2 — Repository naming

### Current name: `cyperx84/claude-skills-mental-models`

The draft brief surfaced four problems with the current name, all of which hold up:

1. **Misleading scope.** The repo no longer ships only a Claude skill. It ships a CLI, a Python library, an MCP server, and a portable AgentSkills variant. The name undersells 4 of 5 surfaces.
2. **Harness-coupled identity.** The `claude-skills-*` prefix ties the project to one harness, but the MCP server works in Cursor, Zed, Continue, OpenCode, Cline, and OpenClaw — see [`docs/mcp/`](../mcp/).
3. **PyPI / CLI mismatch.** The package is already published as `mental-models` ([`packages/mental_models/pyproject.toml`](../../packages/mental_models/pyproject.toml)) and `mental-models-mcp`. The repo URL should echo the install name so `pip install mental-models` and `github.com/cyperx84/mental-models` match. This is the single concrete reason worth renaming for.
4. **Awkward shape.** "claude-skills-mental-models" reads like a sub-directory path, not a project.

### Recommendation: rename to `cyperx84/mental-models`

Ranked options considered:

1. **`mental-models`** *(recommended)*. Matches the PyPI name, matches the CLI entry point, matches how users describe it. Short, memorable, SEO-friendly. The only risk: the slug may already be taken under the account. If so, see fallbacks.
2. **`latticework`**. Distinctive, Munger-native, strong brand. Downside: doesn't say what it does; users searching "mental models Claude skill" won't find it without tags.
3. **`mental-models-kit`**. Keeps the brand, signals "more than a library". Reasonable compromise.
4. **`munger`**. Punchy but trades on a person's name — harder to explain.
5. **Keep `claude-skills-mental-models`**. Justified only if you want to stay discoverable inside a `claude-skills-*` naming convention used by specific aggregators. If so, add rich repo topics (`mental-models`, `mcp-server`, `claude-skill`, `cli`, `reasoning`) instead of renaming.

### Migration checklist

Once the GitHub rename is done (Settings → rename), GitHub auto-redirects the old URL — no broken links. Before the rename, the 21 occurrences of `claude-skills-mental-models` across 11 files have been updated in this repo so the switch is zero-friction. The still-manual steps are:

1. **GitHub:** rename the repo via Settings → `General` → Repository name → `mental-models`.
2. **Verify** one old URL (e.g. the v0.2.0 release page) redirects correctly.
3. **PyPI:** no action required — the package is already `mental-models`; updated project URLs in `pyproject.toml` ship on the next release.
4. **Downstream harness docs** (Cursor/Zed/Continue/OpenCode configs in `docs/mcp/`) need no change — they install by package name, not Git URL.

### Fallback if `cyperx84/mental-models` is taken

Pick in order: `latticework`, then `mental-models-kit`. If neither appeals, keep the current name and fix discoverability with repo topics.

---

## Sources

- <https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking>
- <https://github.com/mettamatt/code-reasoning>
- <https://github.com/ckelsoe/claude-skill-prompt-architect>
- <https://github.com/nidhinjs/prompt-master>
- <https://github.com/VoltAgent/awesome-agent-skills>
- <https://github.com/ComposioHQ/awesome-claude-skills>
- <https://github.com/glebis/claude-skills>
- <https://github.com/AdrienLemaire/awesome-mental-models>
- <https://github.com/WiseCharlie/mental-models>
- <https://modelthinkers.com/mental-model/mungers-latticework>
- <https://mahavak.github.io/models/>
- <https://sourcesofinsight.com/charlie-munger-mental-models/>

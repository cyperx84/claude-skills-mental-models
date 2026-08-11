# SCAN-REPORT — cyperx84/claude-skills-mental-models

Read-only full-tree scan, 2026-07-30. Every file listed under §2 was read directly; nothing here is inferred from the README alone.

---

## 1. WHAT it is

One content corpus — 98 Munger-style mental models — shipped through **five interfaces**:

| Surface | Location | Role |
|---|---|---|
| **Claude Code skill** (primary) | `.claude/skills/mental-models/` | Full skill: `SKILL.md` + `REFERENCE.md` + `PATTERNS.md` + `examples/` (5 worked scenarios) + `models/` (98 md files) + `resources/` (index JSON + quick-reference). Progressive disclosure: SKILL.md is a CLI-orchestration playbook with a file-fallback path. |
| **Portable skill** | `skills/mental-models/` | Lean copy of SKILL.md only, CLI-first, no bundled data. For OpenClaw and any AgentSkills-convention harness (`skills/<name>/SKILL.md`). |
| **CLI** | `packages/mental_models/` → `mental-models` on PyPI | `select / get / list / categories / apply / which / doctor / version`, all with `--json`. **Declared single source of truth.** |
| **MCP server** | `packages/mental_models_mcp/` → `mental-models-mcp` on PyPI | FastMCP stdio server exposing `mm_select / mm_get / mm_list / mm_categories / mm_apply / mm_doctor`. Mirrors the CLI 1:1. |
| **Python library** | same `mental-models` package | `select_models`, `get_model`, `load_index`, `list_categories`, `select_models_with_claude` (optional `[claude]` extra). |

**Source-of-truth topology:**

```
.claude/skills/mental-models/resources/model-index.json   ← canonical DATA
        │  (compile_index.py embeds md sections into it;
        │   sync_package_data.py copies it)
        ▼
packages/mental_models/src/mental_models/data/model-index.json  ← wheel copy
        │
        ▼
CLI (cli.py) ── skill shells out to this
   ▲   ▲
   │   └── MCP server (server.py) — imports mental_models, re-implements helpers
   └── Python lib (index.py, selector.py)
```

The CLI is the claimed source of truth for *logic*, but the **skill directory** is the source of truth for *content* (98 md files + canonical index). That's an important asymmetry: data flows skill → package, logic flows package → skill. The MCP server duplicates three helper functions (`_model_to_dict`, `_read_model_markdown`, `_extract_sections`) from `cli.py` with an explicit "keep in sync" comment — a known drift hazard.

---

## 2. CURRENT ARCHITECTURE

### Directory layout

```
.claude/skills/mental-models/     # primary Claude Code skill (content + playbook)
  SKILL.md                        # 128-line CLI-orchestration playbook + file fallback
  REFERENCE.md                    # 166 lines, per-category deep walkthrough
  PATTERNS.md                     # 171 lines, decision trees by problem shape
  examples/                       # 5 worked scenarios (~40-60 lines each)
  models/                         # 98 md files in 8 Mental_Model_<Category>/ dirs + _TEMPLATE.md
  resources/
    model-index.json              # 258 KB, THE canonical data artifact
    quick-reference.md            # 251 lines, problem→model lookup tables
skills/mental-models/SKILL.md     # portable copy (112 lines, CLI-only, no data)
packages/
  mental_models/                  # CLI + lib (hatchling, uv, zero deps)
    src/mental_models/{__init__,index,selector,cli}.py
    src/mental_models/data/model-index.json   # 258 KB copy (drift-checked in CI)
    tests/ (3 files)
  mental_models_mcp/              # MCP wrapper (deps: mental-models>=0.2.0, mcp>=1.0)
    src/mental_models_mcp/{__init__,__main__,server}.py
    tests/ (2 files)
scripts/                          # 4 stdlib-only Python scripts
evals/                            # two eval harnesses + cases + judge
docs/                             # categories.md, demo.gif/.tape, latticework.{json,mmd,svg},
  mcp/ (6 client config snippets), openclaw/README.md
.github/workflows/                # validate.yml, publish.yml, evals.yml
```

Total Python: ~2,658 LOC. Content: 98 model md files (~2–3 KB each, template-enforced 5 bold-label sections).

### How content is stored/encoded

- Each model = one md file, e.g. `models/Mental_Model_General/m07_inversion.md`, with 5 bold-label sections: `**Description:**`, `**Keywords for Situations:**`, `**Thinking Steps:**`, `**Coaching Questions:**`, `**When to Avoid (or Use with Caution):**`.
- `model-index.json` (258 KB) holds all 98 entries: `{id, name, slug, category, path, keywords[], summary, thinking_steps, coaching_questions, when_to_avoid}` — i.e. **the full prose of 3 of the 5 sections is denormalized into the JSON**. `scripts/compile_index.py` re-extracts those sections from the md files and rewrites the JSON; `validate_models.py` fails CI on any drift between md and JSON. So content is stored **twice** (md files + embedded in JSON), kept consistent by a compile step plus a CI gate.
- Section extraction is done by the **same 5-regex block copy-pasted into 4 places**: `compile_index.py`, `validate_models.py`, `cli.py:_extract_sections`, `server.py:_extract_sections`.

### How selection works

`selector.py`: pure-Python keyword scorer, zero deps, deterministic.

- Tokenize query (ASCII-only regex, stopword list, hand-rolled suffix stemmer with an irregulars table, hyphen subword splitting).
- Per model, token sets cached module-level (`_MODEL_TOKEN_CACHE`).
- Score: name-token hit +4, keyword hit +3, description token +1, substring-in-description +0.5, model-name-in-query +5. Sort by `(-score, slug)`, take top-k.
- `select_models_with_claude` optionally replaces this with an Anthropic API call (falls back to keywords on any failure).
- Regression coverage: `evals/selector_cases.jsonl` (30 cases) run in CI by `run_selector_evals.py` — deterministic, no API key.

### Build/packaging flow

1. Edit model md files.
2. `python scripts/compile_index.py` — re-embed sections into canonical JSON.
3. `python scripts/sync_package_data.py` — copy canonical JSON into the wheel's data dir.
4. `scripts/validate_models.py` — frontmatter + sections + index↔disk + md↔JSON drift + package-sync drift, all in one gate (CI: `validate.yml`).
5. `scripts/build_latticework.py` — shared-keyword graph → `docs/latticework.{json,mmd}` + core subgraph; CI fails if the committed artifacts drift (`git diff --exit-code`).
6. `uv build` per package; hatchling force-includes the JSON into the wheel.

### Release flow (`RELEASING.md`)

Bump `packages/mental_models/pyproject.toml` version → CHANGELOG → sync data → local test/build → tag `vX.Y.Z` → GitHub Release → `publish.yml` (OIDC Trusted Publishing, no tokens; TestPyPI via manual dispatch). **Only `mental-models` is published by the workflow — `mental-models-mcp` has no publish job** despite RELEASING.md/README claiming PyPI availability for both.

---

## 3. COMPLEXITY AUDIT

### Where the complexity lives

1. **Double storage of content.** 98 md files AND the same prose embedded in `model-index.json` (which is why the index is 258 KB). This exists so wheel installs are self-contained (no md files shipped in the package). Cost: a compile step, a sync step, a drift validator, and CI gates — four moving parts to keep two copies of the same text identical.
2. **Four copies of the section-extraction regex block.** Any change to the md format (e.g. renaming a bold label) must be edited in `compile_index.py`, `validate_models.py`, `cli.py`, and `server.py`. Miss one and you get silent divergence between what the compiler embeds and what the CLI parses at runtime.
3. **Three-way index path resolution** (`index.py:_candidate_paths`): walk up from cwd, walk up from `__file__`, bundled data. The cwd walkup means `mental-models` behaves differently depending on which directory you invoke it from — a dev-mode nicety that's also a debugging trap (doctor exists largely to diagnose this).
4. **MCP/CLI helper duplication** with "keep in sync" comments — drift by design.
5. **Fallback paths everywhere.** SKILL.md has CLI path + file-fallback path. CLI `apply`/`get` parse live md from disk when present ("dev mode") and fall back to embedded JSON sections. Selector has keyword path + optional Claude path. Evals have SDK + CLI generator, judge + substring grader. Each fallback doubles the test surface.
6. **Five distribution surfaces for ~2,600 LOC and one JSON file.** Each surface needs its own README, install docs, config snippets (6 MCP client JSONs), and precedence docs (`skills/README.md`).

### What's redundant

- **`resources/quick-reference.md` vs `PATTERNS.md` vs the Discovery Heuristics table in SKILL.md** — three overlapping problem→model lookup guides maintained by hand.
- **`docs/categories.md` vs `mental-models list`/`categories` vs the category tables in README + SKILL.md** — the same catalog rendered four times.
- **`latticework.{json,mmd,svg}` + mermaid block pasted into README.md** — generated artifacts committed to the repo, with a CI drift gate. The README copy is a hand-pasted snapshot of `latticework_core.mmd` (already stale in class names: `c_Physics__Chemistry__` vs actual categories).
- **`select_models_with_claude`** — an LLM picker inside a tool whose entire premise is that the calling agent (Claude Code, etc.) is already an LLM doing the reasoning. Dead weight per the owner's own "CLI never calls an LLM" doctrine.
- **File-fallback section of `.claude/skills/mental-models/SKILL.md`** — the CLI is on PyPI; `uvx mental-models` runs with no install. The fallback duplicates REFERENCE.md's purpose.

### What breaks if simplified

- **Removing md→JSON embedding** breaks wheel self-containment: `apply`/`get` need section prose at runtime with no md files in the package. Fix requires either shipping md files as package data instead (simpler — see §4) or keeping the compile step.
- **Removing cwd-walkup resolution** breaks the dev loop where repo edits are live without reinstalling.
- **Cutting the MCP server** loses Claude Desktop/Cursor/Zed/Continue users who can't load Claude Code skills — it's the only surface those clients can consume. (Though per the owner's doctrine, a CLI on PATH covers most of this via `uvx`.)
- **Cutting the portable `skills/` copy** loses AgentSkills-convention harnesses that don't read `.claude/skills/`.
- **Removing evals** removes the only regression signal for the selector (30 deterministic cases are cheap and genuinely useful).

### vs 2025–2026 standards

- **Claude Code skills**: the repo predates the current plugin marketplace convention. There is **no `.claude-plugin/plugin.json`** — distribution is "clone + symlink," which is the pre-marketplace pattern. Current standard: a plugin repo with `plugin.json` + skills under the plugin root, installable via `/plugin marketplace add`. The skill's own structure (SKILL.md frontmatter, progressive disclosure, bundled resources) is compliant and good.
- **AgentSkills spec** (agentskills.io-style `skills/<name>/SKILL.md` with YAML frontmatter): the portable `skills/mental-models/SKILL.md` follows it correctly. This part is already modern.
- **MCP**: FastMCP with tool names + descriptions is current practice. Stdio-only is fine for local tools.
- **Packaging**: uv + hatchling + Trusted Publishing is exactly the 2025–26 standard. Good.
- **Overall**: the *formats* are modern; the *packaging/distribution* is one generation behind (no plugin manifest, manual symlinks), and the *content pipeline* (double storage + compile/sync/validate) is homegrown complexity that a simpler encoding would eliminate.

---

## 4. REFACTOR ASSESSMENT

Honest opinion: **the idea is sound, the CLI-first architecture is right, and ~60% of the repo is scaffolding that exists only because content is stored in two formats.** A rewrite can cut the repo roughly in half without losing a single capability users touch.

### The simplest possible version

**One data file. One package. Two thin wrappers.**

1. **Content: keep the 98 md files as the only source of content** — they're well-written, template-consistent, and diff-friendly. But ship them **inside the Python package** as package data (`mental_models/data/models/*.md` — flat, category in frontmatter or filename). Delete the embedded-prose JSON entirely: build the index **at import time** by parsing the 98 bundled md files once (lru_cache). 98 × 3 KB parse is single-digit milliseconds — the pre-compiled JSON buys nothing a wheel can't compute on first load. This deletes: `compile_index.py`, `sync_package_data.py`, the drift half of `validate_models.py`, the 258 KB JSON duplication, and 3 of the 4 regex-block copies (one parser lives in the package; everyone imports it).
2. **Package: one package, not two.** Fold the MCP server into `mental-models` as `python -m mental_models.mcp` or a `mental-models-mcp` extra entry point (`pip install mental-models[mcp]`). Deletes: a second pyproject, second README, second test dir, the uv path-dependency override, the duplicated helpers, and the unpublished-package problem.
3. **Skill: one skill, not two.** Ship the AgentSkills-standard `skills/mental-models/SKILL.md` as canonical (that layout works in OpenClaw *and* is the emerging cross-harness standard), and distribute to Claude Code via a **`.claude-plugin/plugin.json`** marketplace plugin that references it. Delete the `.claude/skills/` vs `skills/` split and the file-fallback section (CLI via `uvx` is always available; if it truly isn't, `get`/`apply` JSON output is reproducible by the agent reading the same files the CLI reads — one sentence of guidance suffices).
4. **Keep**: `selector.py` as-is (small, tested, deterministic — the crown jewel); the CLI subcommand set as-is (good interface); the 30-case deterministic selector eval in CI; `validate_models.py` reduced to "md files parse + template sections present"; uv/hatchling/Trusted Publishing; REFERENCE.md + PATTERNS.md + examples (genuinely useful progressive disclosure — but drop quick-reference.md, merged into PATTERNS.md).
5. **Cut**: `select_models_with_claude` + `[claude]` extra (violates own doctrine; the harness LLM already reasons); latticework generation pipeline or at least stop gating CI on committed generated artifacts (regenerate on docs builds only); `docs/categories.md` (regenerate from `mental-models list`); the LLM-judge eval harness (`run_evals.py`, `judge.py`, `evals.yml`) — 15 cases, costs API money, manual-only, and its signal is largely covered by the deterministic selector evals. Archive it if sentimental.

### Target structure

```
mental-models/                     # repo root = one uv project
  pyproject.toml                   # name: mental-models, extras: [mcp], [dev]
  src/mental_models/
    __init__.py  index.py  selector.py  cli.py  mcp.py   # mcp.py = today's server.py, helpers shared
    data/models/*.md               # 98 md files, the ONLY content store
  skills/mental-models/SKILL.md    # AgentSkills-standard, CLI-first (canonical skill)
  .claude-plugin/plugin.json       # Claude Code marketplace manifest → same skill
  tests/                           # merged test suite
  evals/selector_cases.jsonl + run_selector_evals.py
  docs/                            # demo.gif, README assets
  scripts/validate_models.py       # template/parse check only
  .github/workflows/{validate,publish}.yml
```

Roughly: 5 surfaces → 3 (CLI/lib, MCP entry point, one skill distributed two ways); 4 regex copies → 1; 2 pyprojects → 1; ~2,650 Python LOC → ~1,800; content stored once.

### Migration risks (be honest)

- **Slug/path compat**: `path` fields in the JSON point at `models/Mental_Model_<Category>/...`; external users may rely on `get` markdown output shape. Keep output schemas byte-compatible; the refactor changes where bytes live, not what the CLI emits.
- **Import-time parse**: parsing 98 md files on first `load_index()` must stay lazy + cached, or every CLI call pays it. It already is (`lru_cache`); keep that.
- **Skill users on old layout**: anyone who symlinked `.claude/skills/mental-models/` breaks. Provide one release that keeps a stub at the old path pointing to the new location, and call it out in CHANGELOG.
- **PyPI naming**: `mental-models-mcp` is already claimed on PyPI (per README); folding it into extras orphans that name. Deprecate it with a final shim release that depends on `mental-models[mcp]`.

### Bottom line

Don't rewrite the *logic* — selector and CLI are good. Rewrite the *plumbing*: single content store (bundled md files, parse at import), single package with an MCP extra, single canonical skill with a plugin manifest for Claude Code. That gets you to current plugin/AgentSkills standards, deletes the compile/sync/drift class of bugs entirely, and halves the maintenance surface. The 98 model files and the selector are the asset; everything else is scaffolding around a data-duplication decision that no longer needs to exist.

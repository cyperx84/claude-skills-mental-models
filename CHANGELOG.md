# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2026-09-07

### Fixed
- **Retrieval was unresolvable from the catalog.** `SKILL.md` and `CATALOG.md` told the
  agent to read `models/<Category_Dir>/<mNN>_<slug>.md`, but the catalog supplies only the
  slug — never the number or the directory — and its sections are not in ID order, so an
  agent inferring `mNN` from position guessed wrong. Retrieval is now a glob,
  `models/*/m??_<slug>.md`, verified to resolve uniquely for all 98 slugs.
- `SKILL.md` claimed `CATALOG.md`'s headings gave the exact category-directory mapping. They
  do not match the directory names or the Category Map. The glob removes the need for it.
- The five worked examples cited "Tree 1"–"Tree 6", a scheme defined only in the deleted
  `PATTERNS.md`. Step 2 now points the agent at `examples/`, so it was reading reasoning
  that referenced nothing. Rewritten to name the discovery heuristics in `SKILL.md`.
- `REFERENCE.md` listed Incentives as `m19 / m79`; m79 is envy and jealousy. Corrected to
  m77 `bias_from_incentives`. Its Mathematics section also named "compounding" and "power
  laws", neither of which exists — replaced with the real m44–m47.
- `SKILL.md` told the agent to read user models' *headings*; a template-conformant model has
  exactly one, so user models were being selected on filename alone. Now says to read the
  file, or at minimum its **Keywords for Situations** line.
- Removed `docs/demo.gif` — it demoed `uvx`/`mental-models select`, commands this release
  deletes, nine lines above "no dependencies, no runtime, no build step". Its `.tape` source
  was deleted too, so it could not be re-recorded.
- Removed `.markdownlint.jsonc`; nothing consumes it now that the workflows are gone.
- Noted in CONTRIBUTING that `docs/latticework.svg` is a static snapshot whose generator and
  input data no longer exist.

Found by an independent review of #12.

## [1.1.0] - 2026-09-07

### Added
- **Bring your own mental models.** The skill now globs `.mental-models/*.md` (working
  directory) and `~/.claude/mental-models/*.md` (personal) alongside the bundled 98. A user
  model wins any slug collision with a built-in. Neither path is touched by a plugin
  update, so user models survive upgrades. No config, no registration, no code — the
  bundled corpus is a starting set, not a fixed list.
- `models/_TEMPLATE.md` rewritten as a user-facing format spec rather than a contributor
  note: where to put the file, and why **When to Avoid** is the section that matters.

### Notes
- Verified end-to-end: a project-local `blast_radius_first.md` was selected, led the
  analysis, had its Thinking Steps walked in order and its When to Avoid applied, and was
  combined with three bundled models from other categories.

## [1.0.0] - 2026-09-07

Collapsed the repo to what actually worked: a skill and a plugin manifest.

### Removed
- The Python package (`packages/mental_models/`, restructured to `src/mental_models_kit/`
  earlier on this branch), its CLI, and its 1,089-line test suite.
  2,115 lines of source wrapped around markdown that the agent reads directly. Never
  published to PyPI, never had a user.
- The MCP server and its per-client config docs (`docs/mcp/`).
- The eval harness (`evals/`), corpus validator and latticework generator (`scripts/`),
  and the CI workflows that ran them.
- `PATTERNS.md` and `docs/categories.md` — a third and fourth index of the same 98 models.
  `CATALOG.md` is the index; SKILL.md carries the discovery heuristics.
- Planning artifacts now spent: `REBUILD-PLAN.md`, `DEMAND-REPORT.md`, `SCAN-REPORT.md`,
  `RELEASING.md`, `docs/openclaw/`.

### Migration
- **If you symlinked `.claude/skills/mental-models` into `~/.claude/skills/`, repoint it at
  `skills/mental-models`.** That directory no longer exists, and a dangling symlink fails
  silently — the skill stops activating with no error. Or install the plugin instead.

### Changed
- `SKILL.md` no longer mentions a CLI. Retrieval is reading a file path.
- Install is `/plugin marketplace add cyperx84/claude-skills-mental-models` plus
  `/plugin install mental-models@mental-models`. Other harnesses symlink
  `skills/mental-models/`.
- `plugin.json` and `marketplace.json` filled out against the documented schemas
  (version, license, author on both).
- README and CONTRIBUTING rewritten; both described packages that no longer exist.

### Notes
- The skill `description` frontmatter is unchanged and hardcodes "98 mental models". It is
  the activation trigger, so it moves only as a deliberate, measured change.
- The 98 model files are untouched. They all landed in the initial commit (2025-10-31) and
  have had exactly one content edit since; rewriting them with real citations and real
  failure cases is the next piece of work, tracked separately.

## [0.2.0] - 2026-04-09

### Added
- `mental-models-mcp` server package (`packages/mental_models_mcp/`) exposing the latticework to Claude Desktop, Cursor, Zed, Continue, Cline, and any MCP-capable harness.
- Full CLI subcommands: `select`, `get`, `list`, `categories`, `apply`, `which`, `doctor`, `version` — all with `--json` for deterministic, scriptable output.
- Deterministic selector eval harness (`evals/run_selector_evals.py`) with 30 regression cases, wired into CI.
- Rewritten `README.md` with installation, usage, and contribution guidance (2026-04-09).
- Progressive disclosure refactor of `mental-models/SKILL.md` so the model loads a compact index first and pulls full model details on demand.
- CI validation workflow under `.github/workflows/` to lint `SKILL.md` frontmatter and validate `model-index.json`.
- Evaluation harness in `evals/` (`cases.jsonl`, `run_evals.py`, `README.md`) for regression testing skill activation and model selection quality.
- Community files: `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, issue and PR templates.
- `REFERENCES.md` listing primary and secondary sources for the 98 mental models.
- `evals/MODERNIZATION.md` capturing modernization opportunities and decisions.

### Changed
- `SKILL.md` refactored as a CLI-orchestration playbook: it shells out to `mental-models` as the single source of truth and falls back to bundled files only when the CLI is unavailable. Works in any harness.
- Selector tokenizer now emits hyphen subwords so multi-word queries like "first principles" correctly match slugs like `first-principle_thinking`.
- Repository reorganized as a multi-skill workspace under `.claude/skills/`.
- `SKILL.md` description tuned for sharper model-invoked activation.

### Fixed
- CLI edge cases: unicode-safe queries, empty/stopword-only queries handled gracefully, 10KB+ queries truncate cleanly, `--top` validation, slug whitespace/case normalization in `get`/`apply`, and `apply --json` always emits all four canonical sections even when the source model is partial.
- `select_models(top_k=-1)` previously returned all-but-last model due to a slice bug; now clamps to `[]`.

## [0.1.0] - 2025-10-01

### Added
- Initial release of the `mental-models` skill with Charlie Munger's latticework of 98 mental models.
- `resources/model-index.json` catalog covering Art, Economics, General Thinking Tools, Human Nature & Judgment, Mathematics, Physics/Chemistry/Biology, Systems Thinking, Military & Strategy, and more.
- `resources/quick-reference.md` cheat sheet.
- MIT `LICENSE`.

[1.1.1]: https://github.com/cyperx84/claude-skills-mental-models/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/cyperx84/claude-skills-mental-models/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/cyperx84/claude-skills-mental-models/compare/v0.2.0...v1.0.0
[0.2.0]: https://github.com/cyperx84/claude-skills-mental-models/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/cyperx84/claude-skills-mental-models/releases/tag/v0.1.0

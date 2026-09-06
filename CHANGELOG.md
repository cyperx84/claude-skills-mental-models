# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- The Python package (`src/mental_models_kit/`), its CLI, and its 1,089-line test suite.
  2,115 lines of source wrapped around markdown that the agent reads directly. Never
  published to PyPI, never had a user.
- The MCP server and its per-client config docs (`docs/mcp/`).
- The eval harness (`evals/`), corpus validator and latticework generator (`scripts/`),
  and the CI workflows that ran them.
- `PATTERNS.md` and `docs/categories.md` — a third and fourth index of the same 98 models.
  `CATALOG.md` is the index; SKILL.md carries the discovery heuristics.
- Planning artifacts now spent: `REBUILD-PLAN.md`, `DEMAND-REPORT.md`, `SCAN-REPORT.md`,
  `RELEASING.md`, `docs/openclaw/`.

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

[1.1.0]: https://github.com/cyperx84/claude-skills-mental-models/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/cyperx84/claude-skills-mental-models/compare/v0.2.0...v1.0.0
[0.2.0]: https://github.com/cyperx84/claude-skills-mental-models/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/cyperx84/claude-skills-mental-models/releases/tag/v0.1.0

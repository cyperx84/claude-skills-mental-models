# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.2.0]: https://github.com/cyperx84/claude-skills-mental-models/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/cyperx84/claude-skills-mental-models/releases/tag/v0.1.0

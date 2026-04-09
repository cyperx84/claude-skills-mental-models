# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Rewritten `README.md` with installation, usage, and contribution guidance (2026-04-09).
- Progressive disclosure refactor of `mental-models/SKILL.md` so the model loads a compact index first and pulls full model details on demand.
- CI validation workflow under `.github/workflows/` to lint `SKILL.md` frontmatter and validate `model-index.json`.
- Evaluation harness in `evals/` (`cases.jsonl`, `run_evals.py`, `README.md`) for regression testing skill activation and model selection quality.
- Community files: `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, issue and PR templates.
- `REFERENCES.md` listing primary and secondary sources for the 98 mental models.
- `evals/MODERNIZATION.md` capturing modernization opportunities and decisions.

### Changed
- Repository reorganized as a multi-skill workspace under `.claude/skills/`.
- `SKILL.md` description tuned for sharper model-invoked activation.

## [0.1.0] - 2025-10-01

### Added
- Initial release of the `mental-models` skill with Charlie Munger's latticework of 98 mental models.
- `resources/model-index.json` catalog covering Art, Economics, General Thinking Tools, Human Nature & Judgment, Mathematics, Physics/Chemistry/Biology, Systems Thinking, Military & Strategy, and more.
- `resources/quick-reference.md` cheat sheet.
- MIT `LICENSE`.

[Unreleased]: https://github.com/cyperx/claude-skills-mental-models/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/cyperx/claude-skills-mental-models/releases/tag/v0.1.0

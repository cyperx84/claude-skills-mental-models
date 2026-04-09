# Modernization Notes

Tracking opportunities considered while updating the `mental-models` skill for the
current Claude Code ecosystem. Not every item is in scope for the current release.

## Done

- **Progressive disclosure.** `SKILL.md` now loads a compact index and the model
  pulls `resources/model-index.json` entries on demand instead of all 98 descriptions
  at once. Keeps the default-context budget small.
- **Description field tuning.** The `description` frontmatter was rewritten to
  include concrete trigger phrases ("help me think", "apply mental model", specific
  model names) so the router picks the skill up more reliably.
- **CI validation.** A GitHub Actions workflow lints frontmatter and validates
  `model-index.json` shape on every PR.
- **Evals.** See `evals/` for the regression harness and `cases.jsonl`.

## Considered

- **Compatibility with Claude 4.x family.** The skill format is model-agnostic but
  activation behavior differs across Sonnet 4.6, Opus 4.6, and Haiku 4.5. The eval
  harness should eventually pin the model via `claude -p --model ...` and run the
  suite against each tier so we can catch tier-specific regressions.
- **Agent SDK integration.** The Anthropic Agent SDK exposes skills
  programmatically; a thin wrapper could expose `select_models(problem: str)` as a
  tool for non-Claude-Code agents. Out of scope for 0.2 but tracked.
- **MCP server wrapper.** An MCP server could serve `model-index.json` as a
  queryable resource so other clients (Cursor, Zed, etc.) can reuse the catalog
  without forking. Nice-to-have; only worth it if external demand shows up.
- **Versioning strategy.** The repo now follows SemVer, tracked via `CHANGELOG.md`.
  Breaking changes = renaming slugs or removing models. Additive changes = new
  models or new categories.
- **Telemetry.** The honest answer to "is this skill actually useful?" is the eval
  suite in `evals/`. We deliberately do not collect runtime telemetry from users;
  regression testing on a curated set of prompts is the signal we optimize for.
  When a new model family ships, re-run evals and diff the results.

# Portable skill (for OpenClaw and other AgentSkills harnesses)

**Claude Code is the primary target** — the canonical skill lives at
[`.claude/skills/mental-models/`](../.claude/skills/mental-models/) with full
progressive disclosure (`REFERENCE.md`, `PATTERNS.md`, `examples/`, `models/`,
`resources/`).

This `skills/mental-models/` directory is a **lean, portable copy** for harnesses
that follow the AgentSkills convention (`skills/<name>/SKILL.md`) but don't know
about `.claude/skills/`. It is CLI-first: it shells out to the `mental-models`
Python CLI (which you install with `pip install mental-models` or run via
`uvx mental-models`) and carries no bundled data files of its own. All content
still comes from the one source of truth — the CLI's data package.

## Supported harnesses

- **OpenClaw** — drops into `<workspace>/skills/mental-models/` or
  `~/.openclaw/skills/mental-models/`. See
  [`docs/openclaw/README.md`](../docs/openclaw/README.md).
- **Any AgentSkills-compatible harness** — point it at this directory.

## Precedence

1. `.claude/skills/mental-models/` — Claude Code, full feature set
2. `skills/mental-models/` — OpenClaw and portable harnesses, CLI-backed
3. `packages/mental_models_mcp/` — MCP server for Claude Desktop, Cursor, Zed,
   Continue, Cline, and anything else that speaks MCP

All three talk to the same `mental-models` CLI, so the latticework logic lives
in exactly one place.

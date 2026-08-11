# The `mental-models` skill

> **⚠️ Package not published yet (2026-08).** `mental-models-kit` is not on PyPI. Any
> `pip install` / `uvx` command is a **planned** interface, not a working one, until a real
> release lands and this note is updated to say so. The skill itself needs no install at
> all — see below. See `DEMAND-REPORT.md` for how the project got here.

[`mental-models/`](./mental-models/) is **the** skill — one directory, self-contained, no
build step, no package to fetch. It works by being cloned, symlinked, or copied onto disk;
nothing needs installing for the skill itself to work. This is deliberate: the file-fallback
path (an agent reading `models/*.md` directly) is what every star on this repo was earned by,
and it stays the primary, load-bearing path — not a fallback for when something else fails.

Everything a consumer needs lives inside `mental-models/`:

```
mental-models/
├── SKILL.md          entry point — how and when to use this skill
├── CATALOG.md         all 98 models by slug + keywords, for selection
├── REFERENCE.md        per-category deep walkthrough
├── PATTERNS.md         decision trees by problem shape
├── examples/           5 worked scenarios
└── models/             the 98 source model files (the actual content)
```

## Install (pick one — all reach the same directory)

**Claude Code** — symlink or copy into `~/.claude/skills/`:

```bash
git clone https://github.com/cyperx84/claude-skills-mental-models.git
ln -s "$(pwd)/claude-skills-mental-models/skills/mental-models" ~/.claude/skills/mental-models
```

**OpenClaw and other AgentSkills-convention harnesses** — same directory, different target:

```bash
ln -s "$(pwd)/claude-skills-mental-models/skills/mental-models" <workspace>/skills/mental-models
```

Per-harness detail: [`docs/openclaw/README.md`](../docs/openclaw/README.md).

**Any other tool that just reads files** — point it at `skills/mental-models/`, or copy the
directory somewhere the tool can see it. There is no dependency to resolve either way.

## `.claude/skills/mental-models` — the legacy path, kept working

Earlier releases of this repo put the canonical skill at
`.claude/skills/mental-models/`. That path still exists as a **committed symlink** to
`skills/mental-models/`, so:

- if you (or your fork) already symlinked `~/.claude/skills/mental-models` to
  `<clone>/.claude/skills/mental-models`, that keeps resolving — the symlink hop is
  transparent
- new installs should point at `skills/mental-models/` directly (above); it is now the one
  real copy on disk

## CLI and MCP server — accelerants, not dependencies

The `mental-models` CLI (package `mental-models-kit`) and `mental-models-mcp` server give
deterministic, scriptable retrieval — exact-slug lookup, JSON output, an MCP tool surface for
clients that speak that protocol. **Neither is required.** An agent with only file-read
access gets the identical model content by following `SKILL.md`'s file-fallback path. Status
of the packaged interfaces is tracked in the root [`README.md`](../README.md#install).

## Contributing

Model content itself (the 98 `.md` files under `models/`) does not change in normal
contributions — see the root [`CONTRIBUTING.md`](../.github/CONTRIBUTING.md). Fixes to
`SKILL.md`, `REFERENCE.md`, `PATTERNS.md`, or `examples/` are welcome.

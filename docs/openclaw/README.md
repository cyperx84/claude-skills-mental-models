# OpenClaw integration

> **⚠️ Not published (2026-08).** The `mental-models` and `mental-models-mcp` names on
> PyPI do **not** belong to this project — `mental-models` is an unrelated 2020 package
> and `mental-models-mcp` does not exist. Any `pip install` / `uvx` instruction below is
> **not yet valid**; it installs the wrong software or fails. Run from a clone instead.
> The package ships as `mental-models-kit` in the next release. See `DEMAND-REPORT.md`.

`mental-models` is a **first-class Claude Code skill**; OpenClaw and other
AgentSkills-compatible harnesses are a well-supported second target. The portable
skill at [`skills/mental-models/`](../../skills/mental-models/) is CLI-first and
works in any harness that loads `SKILL.md` files.

## Prerequisite

The portable skill shells out to the `mental-models` CLI, so install that first:

The package is not on PyPI yet, so install from a clone:

```bash
git clone https://github.com/cyperx84/claude-skills-mental-models.git
cd claude-skills-mental-models
uv tool install .           # installs `mental-models` from source
```

Verify:

```bash
mental-models doctor --json
# → {"ok": true, "models": 98, "source": "bundled", ...}
```

## Install the skill in OpenClaw

OpenClaw loads skills from (in precedence order):

1. `<workspace>/skills/`
2. `~/.openclaw/skills/`
3. bundled skills
4. any path listed in `skills.load.extraDirs` in `~/.openclaw/openclaw.json`

Pick whichever fits. The easiest is a symlink from your workspace:

```bash
# clone once
git clone https://github.com/cyperx84/claude-skills-mental-models.git ~/src/mental-models

# symlink into your OpenClaw workspace
ln -s ~/src/mental-models/skills/mental-models <your-workspace>/skills/mental-models
```

Or copy the directory if you prefer a pinned snapshot:

```bash
cp -R ~/src/mental-models/skills/mental-models <your-workspace>/skills/
```

Or point `skills.load.extraDirs` at the checkout:

```jsonc
// ~/.openclaw/openclaw.json
{
  "skills": {
    "load": {
      "extraDirs": ["/home/you/src/mental-models/skills"]
    }
  }
}
```

## Verify

In an OpenClaw session:

```text
/skills list
```

You should see `mental-models`. Then:

```text
help me think through whether to take this new job
```

The skill should activate and shell out to `mental-models select ...`.

## MCP alternative

If you'd rather use the MCP server (programmatic tool surface instead of a
skill-level instruction), see
[`docs/mcp/README.md`](../mcp/README.md) and use the opencode-compatible MCP
client. OpenClaw also supports MCP servers via `mcp.servers`:

```jsonc
// ~/.openclaw/openclaw.json
{
  "mcp": {
    "servers": {
      "mental-models": {
        "command": "uvx",
        "args": ["mental-models-mcp"]
      }
    }
  }
}
```

Or set it live:

```text
/mcp set mental-models="{\"command\":\"uvx\",\"args\":[\"mental-models-mcp\"]}"
```

The skill route is recommended — it gives the agent activation guidance, not
just tools.

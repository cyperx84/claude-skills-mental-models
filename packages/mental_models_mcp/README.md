# mental-models-mcp

> **⚠️ Not published (2026-08).** The `mental-models` and `mental-models-mcp` names on
> PyPI do **not** belong to this project — `mental-models` is an unrelated 2020 package
> and `mental-models-mcp` does not exist. Any `pip install` / `uvx` instruction below is
> **not yet valid**; it installs the wrong software or fails. Run from a clone instead.
> The package ships as `mental-models-kit` in the next release. See `DEMAND-REPORT.md`.

An [MCP](https://modelcontextprotocol.io) server that exposes Charlie Munger's
latticework of mental models to any MCP-capable agent harness — Claude Desktop,
Cursor, Zed, Continue, Cline, OpenCode, and more.

It's a thin wrapper around the [`mental-models`](https://github.com/cyperx84/claude-skills-mental-models)
Python library: same data, same selection logic, exposed as tool calls.

## Install

```bash
# From PyPI (once published)
uv add mental-models-mcp
# or
pip install mental-models-mcp
# or zero-install
uvx mental-models-mcp
```

Pre-release (from this repo):

```bash
pip install -e packages/mental_models_mcp
# uv users: `uv sync` inside packages/mental_models_mcp picks up the
# sibling `mental-models` package automatically via [tool.uv.sources].
```

## Run

```bash
mental-models-mcp           # stdio server
python -m mental_models_mcp # equivalent
```

The server logs a single startup line to stderr and then speaks JSON-RPC
over stdio.

## Tools

| Tool | Input | Returns |
| --- | --- | --- |
| `mm_select` | `query: str, top_k: int = 5` | Top-k matching models |
| `mm_get` | `slug: str, field?: str` | Full model dict with `markdown`, or one field |
| `mm_list` | `category?: str` | All models, optionally filtered |
| `mm_categories` | — | All category names |
| `mm_apply` | `slug: str, problem: str` | Structured sections: description, thinking_steps, coaching_questions, when_to_avoid |
| `mm_doctor` | — | Install/index health report |

### Example: `mm_select`

```json
{ "query": "how do I decide between two jobs", "top_k": 3 }
```

Returns:

```json
{
  "query": "how do I decide between two jobs",
  "count": 3,
  "models": [
    { "slug": "opportunity-cost", "name": "Opportunity Cost", "category": "Economics", "...": "..." }
  ]
}
```

### Example: `mm_apply`

```json
{ "slug": "inversion", "problem": "launching a new pricing tier" }
```

Returns `{ description, thinking_steps, coaching_questions, when_to_avoid, ... }`.

## Harness integration

Each harness expects a slightly different config file. Copy-paste snippets
live under [`docs/mcp/`](../../docs/mcp/) in the repo root.

### Claude Desktop

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "mental-models": {
      "command": "uvx",
      "args": ["mental-models-mcp"]
    }
  }
}
```

### Cursor

`.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "mental-models": {
      "command": "uvx",
      "args": ["mental-models-mcp"]
    }
  }
}
```

### Zed

In `settings.json`:

```json
{
  "context_servers": {
    "mental-models": {
      "command": {
        "path": "uvx",
        "args": ["mental-models-mcp"]
      }
    }
  }
}
```

### Continue

`.continue/config.json`:

```json
{
  "experimental": {
    "modelContextProtocolServers": [
      {
        "transport": {
          "type": "stdio",
          "command": "uvx",
          "args": ["mental-models-mcp"]
        }
      }
    ]
  }
}
```

### Cline (VS Code)

Cline reads MCP servers from its settings UI or `cline_mcp_settings.json`:

```json
{
  "mcpServers": {
    "mental-models": {
      "command": "uvx",
      "args": ["mental-models-mcp"]
    }
  }
}
```

## Development

```bash
cd packages/mental_models_mcp
uv sync
uv run pytest
uv build
```

## License

MIT. See [LICENSE](./LICENSE).

Part of [claude-skills-mental-models](https://github.com/cyperx84/claude-skills-mental-models).

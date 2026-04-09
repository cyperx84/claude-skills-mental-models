# MCP harness configs

Drop-in config snippets for using `mental-models-mcp` in any MCP-capable client.
All of them assume you have `uv` installed — `uvx` will fetch and run the server
on demand without a global install.

| Client         | File                  | Config location |
|----------------|-----------------------|-----------------|
| Claude Desktop | `claude_desktop.json` | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) / `%APPDATA%\Claude\claude_desktop_config.json` (Windows) |
| Cursor         | `cursor.json`         | `~/.cursor/mcp.json` (or project `.cursor/mcp.json`) |
| Zed            | `zed.json`            | `~/.config/zed/settings.json` (merge into top-level) |
| Continue       | `continue.json`       | `~/.continue/config.json` (merge into top-level) |
| OpenCode       | `opencode.json`       | `~/.config/opencode/opencode.json` (or project `opencode.json`) |

## Verify

```bash
uvx mental-models-mcp   # should print a startup banner on stderr
```

Then restart the client. The `mm_select`, `mm_get`, `mm_list`, `mm_categories`,
`mm_apply`, and `mm_doctor` tools should appear.

## Alternative: local install

If you'd rather pin a version:

```bash
pip install 'mental-models-mcp>=0.1.0'
```

Then replace `"command": "uvx", "args": ["mental-models-mcp"]` with
`"command": "mental-models-mcp", "args": []`.

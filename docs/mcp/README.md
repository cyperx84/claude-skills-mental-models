# MCP harness configs

> **⚠️ Not published (2026-08).** The `mental-models` and `mental-models-mcp` names on
> PyPI do **not** belong to this project — `mental-models` is an unrelated 2020 package
> and `mental-models-mcp` does not exist. Any `pip install` / `uvx` instruction below is
> **not yet valid**; it installs the wrong software or fails. Run from a clone instead.
> The package ships as `mental-models-kit` in the next release. See `DEMAND-REPORT.md`.

Drop-in config snippets for the mental-models MCP server in any MCP-capable client.

**Which file do I use?**

- **`local_clone.json` — the only one that works today.** It runs the server out of a
  clone via `uv run`, so it needs no published package. Verified 2026-08-12: the server
  answers `server/discover` with `supportedVersions: ["2026-07-28"]`.
- **Every other file below is for after the first release**, when `mental-models-kit`
  exists on PyPI. They use `uvx --from mental-models-kit[mcp] mental-models-mcp`, which
  fails today because the package is not published yet.

| Client         | File                  | Config location |
|----------------|-----------------------|-----------------|
| **Any (works today)** | `local_clone.json` | merge into your client's MCP config |
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

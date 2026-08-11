"""MCP server for mental-models-kit (spec revision 2026-07-28, SDK ``mcp`` 2.x).

Kept in its own subpackage so the ``mcp`` dependency stays optional: the CLI,
the library and the skill all work with nothing installed but the standard
library. Import ``build_server`` only when you actually want a server.
"""
from __future__ import annotations

__all__ = ["build_server", "main"]


def __getattr__(name: str):  # lazy so `import mental_models_kit.mcp` never needs the SDK
    if name in __all__:
        from . import server

        return getattr(server, name)
    raise AttributeError(name)

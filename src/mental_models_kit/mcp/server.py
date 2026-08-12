"""MCP server exposing the 98-model latticework.

Written against **MCP specification revision 2026-07-28** and the ``mcp`` 2.x
Python SDK. Notes that are easy to get wrong, recorded here so the next edit
does not regress them:

* ``MCPServer``, not ``FastMCP`` -- the v1 class was removed outright in SDK v2.
* Every Python field is snake_case (``is_error``, ``ttl_ms``); the wire stays camelCase.
* Roots, Sampling and Logging are deprecated protocol features. None are used.
  Diagnostics go to stderr, which is the migration the spec itself recommends.
* Raising ``MCPError`` is a *protocol* error the model never sees; every other
  exception becomes ``is_error=True`` content the model reads and reacts to.
  **Every argument to every tool here is supplied by the calling model, and a
  bad one is something that model can correct on the next call** -- so all
  argument validation is model-readable, and nothing in this server raises
  ``MCPError``. An earlier revision raised ``-32602`` for a blank slug; that
  was wrong. It hid the one piece of information that would have let the model
  fix its own call, which is the opposite of what the SDK guidance asks for.
  ``MCPError`` is reserved for genuine protocol faults, and this server has
  none of its own.
* ``tools/list`` is deterministically ordered (registration order below is the
  wire order): the spec asks for it, and a stable order lets clients cache and
  raises prompt-cache hit rates.
* The corpus is 98 static documents that change only on release, so every
  cacheable method advertises a long TTL with ``public`` scope.

The models are exposed as **Resources** as well as tools. That is deliberate:
the Skills-over-MCP work (SEP-2640) is Resources-based, so this shape is a short
hop to it -- while depending on nothing that is still unratified.
"""
from __future__ import annotations

import sys
from typing import Any

from mcp.server import MCPServer
from mcp.server.mcpserver.server import CacheHint

from .. import __version__
from ..catalog import FORMATS, catalog_document
from ..corpus import (
    CATEGORIES,
    ModelNotFound,
    UnknownCategory,
    get_model,
    list_categories,
    list_models,
)
from ..render import apply_dict, model_detail_dict, model_dict, walk_dict
from ..search import has_searchable_tokens, search_models

__all__ = ["build_server", "main"]

# The corpus ships with the package and changes only when a release does.
# One hour is conservative for a client session; `public` lets a shared
# intermediary cache it too, since nothing here is user-specific.
_CACHE = CacheHint(ttl_ms=3_600_000, scope="public")
_CACHEABLE = (
    "tools/list",
    "prompts/list",
    "resources/list",
    "resources/read",
    "resources/templates/list",
    "server/discover",
)

_INSTRUCTIONS = """\
98 mental models from Charlie Munger's latticework, across 8 disciplines.

The intended flow is:
  1. mm_catalog  -- read the whole catalog (~4k tokens)
  2. pick 2-4 models YOURSELF, from different categories
  3. mm_get / mm_apply / mm_walk the slugs you picked

Selection is a reasoning task. Do it yourself; do not delegate it to mm_search,
which is a keyword matcher and is wrong on natural-language problems.
"""

# Directory per category key, for callers that want to read the file directly
# rather than go through a tool. Sourced from the one canonical tuple.
_CATEGORY_DIRS = {key: directory for key, _display, directory, _count in CATEGORIES}


def _require_slug(slug: str) -> str:
    cleaned = (slug or "").strip()
    if not cleaned:
        raise ValueError("slug must be a non-empty string. Call mm_catalog for valid slugs.")
    return cleaned


def _fetch(slug: str):
    """Resolve a slug, turning a miss into model-readable content.

    ``ModelNotFound`` stays an ordinary exception so the SDK returns it as
    ``is_error=True`` -- the model reads the message and can retry with a
    corrected slug, which is exactly the behaviour we want here.
    """
    try:
        return get_model(_require_slug(slug))
    except ModelNotFound as e:
        raise ValueError(f"{e}. Call mm_catalog for the list of valid slugs.") from None


def build_server() -> MCPServer:
    mcp = MCPServer(
        name="mental-models",
        title="Mental Models",
        version=__version__,
        instructions=_INSTRUCTIONS,
        cache_hints={method: _CACHE for method in _CACHEABLE},
    )

    # ---- tools, in wire order -------------------------------------------
    # Registration order IS tools/list order. mm_catalog is first because it is
    # the entry point; mm_search is last because it is the fallback.

    @mcp.tool(
        name="mm_catalog",
        title="Catalog",
        description=(
            "THE ENTRY POINT. Returns all 98 models as slug + name + keywords, grouped "
            "by category (~4k tokens). Read it, then pick 2-4 models across different "
            "categories yourself -- cross-category coverage is the whole point of a "
            "latticework. Then call mm_get/mm_apply/mm_walk on the slugs you chose."
        ),
    )
    def mm_catalog(fmt: str = "compact", category: str | None = None) -> str:
        """The compact catalog to select from. fmt is 'compact' or 'slim'."""
        if fmt not in FORMATS:
            raise ValueError(f"unknown format {fmt!r}. Valid formats: {', '.join(FORMATS)}")
        try:
            return catalog_document(fmt=fmt, category=category)
        except UnknownCategory as e:
            raise ValueError(str(e)) from None

    @mcp.tool(
        name="mm_get",
        title="Get model",
        description="Retrieve one model by exact slug or id, with all five sections.",
    )
    def mm_get(slug: str) -> dict[str, Any]:
        return model_detail_dict(_fetch(slug))

    @mcp.tool(
        name="mm_apply",
        title="Apply model",
        description=(
            "Thinking-steps scaffold for one model against a stated problem. Returns "
            "description, thinking_steps, coaching_questions and when_to_avoid. Walk the "
            "thinking steps verbatim and always check when_to_avoid before concluding."
        ),
    )
    def mm_apply(slug: str, problem: str = "") -> dict[str, Any]:
        return apply_dict(_fetch(slug), (problem or "").strip())

    @mcp.tool(
        name="mm_walk",
        title="Walk one step",
        description=(
            "One thinking step at a time, stateless -- you hold the cursor. Call with "
            "step=0 and increment until the result reports done=true. Use when a problem "
            "deserves working through a framework beat by beat rather than all at once."
        ),
    )
    def mm_walk(slug: str, step: int = 0, problem: str = "") -> dict[str, Any]:
        # walk_dict rejects non-int (bool included) and negative cursors. Surface
        # its message to the model rather than a bare traceback.
        try:
            return walk_dict(_fetch(slug), step, (problem or "").strip())
        except (TypeError, ValueError) as e:
            raise ValueError(f"invalid step: {e}") from None

    @mcp.tool(
        name="mm_list",
        title="List models",
        description="List models as slug/name/category, optionally filtered to one category.",
    )
    def mm_list(category: str | None = None) -> list[dict[str, Any]]:
        try:
            return [model_dict(m) for m in list_models(category)]
        except UnknownCategory as e:
            raise ValueError(str(e)) from None

    @mcp.tool(
        name="mm_categories",
        title="Categories",
        description="The 8 categories and how many models each contains.",
    )
    def mm_categories() -> list[dict[str, Any]]:
        return [
            {
                "key": c.key,
                "display": c.display,
                "directory": _CATEGORY_DIRS[c.key],
                "count": c.count,
            }
            for c in list_categories()
        ]

    @mcp.tool(
        name="mm_search",
        title="Keyword search (NOT selection)",
        description=(
            "Best-effort keyword match. THIS IS NOT MODEL SELECTION and must not be used "
            "to choose models for a problem: it ranks 'two_front_war' and "
            "'asymmetric_warfare' in the top 3 for 'how do I decide between two jobs', and "
            "'alloying'/'bubbles' for 'our team keeps missing deadlines'. Use it only to "
            "jog your memory when you half-remember a model's name. To choose models for a "
            "problem, call mm_catalog and decide yourself."
        ),
    )
    def mm_search(query: str, top_k: int = 5) -> list[dict[str, Any]]:
        if type(top_k) is not int or top_k < 1:
            raise ValueError(f"top_k must be an integer >= 1, got {top_k!r}")
        if not has_searchable_tokens(query or ""):
            raise ValueError(
                "query has no searchable terms. Call mm_catalog and select models yourself."
            )
        return [model_dict(m) for m in search_models(query, top_k=top_k)]

    # ---- resources -------------------------------------------------------
    # Resources-shaped so SEP-2640 (skills-over-MCP) is a short hop, without
    # depending on that unratified extension.

    @mcp.resource(
        "mental-models://catalog",
        name="catalog",
        title="Mental models catalog",
        description="All 98 models by slug, name and keywords, grouped by category.",
        mime_type="text/markdown",
    )
    def catalog_resource() -> str:
        return catalog_document()

    @mcp.resource(
        "mental-models://model/{slug}",
        name="model",
        title="One mental model",
        description="The full markdown source of a single model, by slug.",
        mime_type="text/markdown",
    )
    def model_resource(slug: str) -> str:
        return _fetch(slug).markdown

    return mcp


def main() -> None:
    """stdio entry point. Transport config lives on run() in SDK v2."""
    try:
        build_server().run("stdio")
    except KeyboardInterrupt:  # a clean Ctrl-C is not a crash
        print("mental-models mcp: interrupted", file=sys.stderr)


if __name__ == "__main__":  # pragma: no cover
    main()

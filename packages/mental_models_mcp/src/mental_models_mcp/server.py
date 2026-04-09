"""MCP server exposing Charlie Munger's mental models.

Tools mirror the `mental-models` CLI subcommands so any MCP-capable harness
(Claude Desktop, Cursor, Zed, Continue, Cline, OpenCode, ...) can reach the
same latticework the Python library and skill already expose.

Transport: stdio (default). Run with ``mental-models-mcp`` or
``python -m mental_models_mcp``.
"""
from __future__ import annotations

import re
import sys
from typing import Any

from . import __version__


# ---------- dependency guard ----------

def _require_mental_models() -> None:
    try:
        import mental_models  # noqa: F401
    except ImportError:
        sys.stderr.write(
            "mental-models-mcp: the 'mental-models' package is not installed.\n"
            "Install it with:  pip install 'mental-models>=0.2.0'\n"
        )
        raise SystemExit(1)


# ---------- helpers (mirrors mental_models.cli — keep in sync until exposed publicly) ----------

def _model_to_dict(m: Any) -> dict[str, Any]:
    return {
        "slug": m.slug,
        "name": m.name,
        "category": m.category,
        "keywords": list(m.keywords),
        "description": m.description,
        "path": m.path,
        "id": m.id,
    }


def _read_model_markdown(m: Any) -> str:
    """Best-effort read of the model's markdown file.

    Mirrors mental_models.cli._read_model_markdown — keep in sync until
    exposed publicly in a future version.
    """
    if not m.path:
        return ""
    try:
        from mental_models.index import _resolve_index_path  # type: ignore
        index_path = _resolve_index_path()
        skill_dir = index_path.parent.parent
        candidate = (skill_dir / m.path).resolve()
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8")
    except Exception:
        pass
    return ""


def _extract_sections(md: str) -> dict[str, str]:
    """Mirrors mental_models.cli._extract_sections — keep in sync until
    exposed publicly in a future version."""
    if not md:
        return {}
    canonical = [
        ("description", re.compile(r"\*\*Description:\*\*", re.IGNORECASE)),
        ("keywords", re.compile(r"\*\*Keywords[^*]*:\*\*", re.IGNORECASE)),
        ("thinking steps", re.compile(r"\*\*Thinking Steps:\*\*", re.IGNORECASE)),
        ("coaching questions", re.compile(r"\*\*Coaching Questions:\*\*", re.IGNORECASE)),
        ("when to avoid", re.compile(r"\*\*When to Avoid[^*]*:\*\*", re.IGNORECASE)),
    ]
    hits: list[tuple[str, int, int]] = []
    for key, pat in canonical:
        match = pat.search(md)
        if match:
            hits.append((key, match.end(), match.start()))
    hits.sort(key=lambda h: h[2])
    sections: dict[str, str] = {}
    for i, (key, body_start, _) in enumerate(hits):
        body_end = hits[i + 1][2] if i + 1 < len(hits) else len(md)
        sections[key] = md[body_start:body_end].strip()
    return sections


def _safe(fn):
    """Wrap a tool handler so exceptions become ``{"error": "..."}``."""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return fn(*args, **kwargs)
        except Exception as e:  # noqa: BLE001
            return {"error": f"{type(e).__name__}: {e}"}
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper


# ---------- tool handlers (pure functions — unit-testable in-process) ----------

@_safe
def mm_select(query: str, top_k: int = 5) -> dict[str, Any]:
    """Select the top-k mental models most relevant to a free-text query."""
    from mental_models import select_models
    q = (query or "").strip()
    if not q:
        return {"query": q, "count": 0, "models": []}
    results = select_models(q, top_k=top_k)
    return {
        "query": q,
        "count": len(results),
        "models": [_model_to_dict(m) for m in results],
    }


@_safe
def mm_get(slug: str, field: str | None = None) -> dict[str, Any]:
    """Get a model by slug. Returns full dict with 'markdown' field, or a
    single-field projection when ``field`` is provided."""
    from mental_models import get_model
    m = get_model(slug)
    data = _model_to_dict(m)
    if field:
        if field not in data and field != "markdown":
            return {"error": f"unknown field: {field}"}
        if field == "markdown":
            return {"field": "markdown", "value": _read_model_markdown(m)}
        return {"field": field, "value": data[field]}
    data["markdown"] = _read_model_markdown(m)
    return data


@_safe
def mm_list(category: str | None = None) -> dict[str, Any]:
    """List all mental models, optionally filtered by category."""
    from mental_models import load_index
    models = load_index()
    if category:
        models = [m for m in models if m.category.lower() == category.lower()]
    return {
        "count": len(models),
        "models": [_model_to_dict(m) for m in models],
    }


@_safe
def mm_categories() -> dict[str, Any]:
    """List all mental-model categories."""
    from mental_models import list_categories
    cats = list_categories()
    return {"count": len(cats), "categories": list(cats)}


@_safe
def mm_apply(slug: str, problem: str) -> dict[str, Any]:
    """Apply a mental model to a problem. Returns structured sections:
    description, thinking_steps, coaching_questions, when_to_avoid."""
    from mental_models import get_model
    m = get_model(slug)
    md = _read_model_markdown(m)
    sections = _extract_sections(md)
    return {
        "slug": m.slug,
        "name": m.name,
        "category": m.category,
        "problem": (problem or "").strip(),
        "description": sections.get("description") or m.description,
        "thinking_steps": sections.get("thinking steps", ""),
        "coaching_questions": sections.get("coaching questions", ""),
        "when_to_avoid": sections.get("when to avoid", ""),
        "path": m.path,
    }


@_safe
def mm_doctor() -> dict[str, Any]:
    """Diagnose the mental-models install: index path, model count, categories."""
    import mental_models
    from mental_models import load_index, list_categories
    from mental_models.index import _resolve_index_path  # type: ignore

    report: dict[str, Any] = {
        "version": getattr(mental_models, "__version__", "?"),
        "mcp_version": __version__,
        "ok": True,
        "checks": {},
    }
    try:
        path = _resolve_index_path()
        report["checks"]["index_path"] = str(path)
        report["checks"]["index_exists"] = path.is_file()
    except Exception as e:  # noqa: BLE001
        report["ok"] = False
        report["checks"]["index_error"] = str(e)
    try:
        models = load_index()
        report["checks"]["model_count"] = len(models)
        if len(models) < 1:
            report["ok"] = False
    except Exception as e:  # noqa: BLE001
        report["ok"] = False
        report["checks"]["load_error"] = str(e)
    try:
        cats = list_categories()
        report["checks"]["category_count"] = len(cats)
    except Exception as e:  # noqa: BLE001
        report["ok"] = False
        report["checks"]["categories_error"] = str(e)
    return report


TOOL_HANDLERS = {
    "mm_select": mm_select,
    "mm_get": mm_get,
    "mm_list": mm_list,
    "mm_categories": mm_categories,
    "mm_apply": mm_apply,
    "mm_doctor": mm_doctor,
}


# ---------- MCP server (FastMCP) ----------

def _build_server():
    """Build and return a FastMCP server with all tools registered.

    FastMCP is the current (SDK 1.0+) high-level API — chosen over the
    lowlevel Server because it auto-derives JSON schemas from type hints
    and docstrings, which keeps this file small and the tool descriptions
    colocated with the handlers.
    """
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("mental-models")

    # Register each module-level handler under its bare public name so the
    # live tool names match the documented ones (mm_select, mm_get, ...).
    mcp.tool(name="mm_select", description="Select the top-k mental models most relevant to a free-text query or problem statement.")(mm_select)
    mcp.tool(name="mm_get", description="Get a mental model by slug (e.g. 'inversion'). Returns the full model dict including the 'markdown' field; pass 'field' to return just one field.")(mm_get)
    mcp.tool(name="mm_list", description="List all mental models, optionally filtered by category.")(mm_list)
    mcp.tool(name="mm_categories", description="List all mental-model categories.")(mm_categories)
    mcp.tool(name="mm_apply", description="Apply a mental model (by slug) to a problem. Returns structured sections: description, thinking_steps, coaching_questions, when_to_avoid.")(mm_apply)
    mcp.tool(name="mm_doctor", description="Diagnose the mental-models install: resolves index path, loads models, counts categories.")(mm_doctor)

    return mcp


def main(argv: list[str] | None = None) -> int:
    """Entry point. Starts the MCP server on stdio."""
    _require_mental_models()
    sys.stderr.write(
        f"mental-models-mcp v{__version__}: starting stdio server "
        "(tools: mm_select, mm_get, mm_list, mm_categories, mm_apply, mm_doctor)\n"
    )
    sys.stderr.flush()
    try:
        server = _build_server()
    except ImportError:
        sys.stderr.write(
            "mental-models-mcp: the 'mcp' package is not installed.\n"
            "Install it with:  pip install 'mcp>=1.0'\n"
        )
        return 1
    server.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

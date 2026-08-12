"""Contracts for the MCP server (spec revision 2026-07-28, SDK mcp 2.x).

Uses the in-memory ``Client(server)`` pattern that replaced v1's
``create_connected_server_and_client_session()``. No transport, no subprocess.
"""
from __future__ import annotations

import pytest

mcp_sdk = pytest.importorskip("mcp", reason="the [mcp] extra is not installed")

from mcp.client import Client  # noqa: E402

from mental_models_kit.mcp.server import build_server  # noqa: E402

# Every test in this module is async; anyio ships the plugin that runs them.
pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"

# Wire order is part of the contract: the spec asks for a deterministic
# tools/list, and mm_catalog must lead because it is the entry point.
EXPECTED_TOOL_ORDER = [
    "mm_catalog",
    "mm_get",
    "mm_apply",
    "mm_walk",
    "mm_list",
    "mm_categories",
    "mm_search",
]


@pytest.fixture
def server():
    return build_server()


@pytest.fixture
async def client(server):
    async with Client(server) as c:
        yield c


async def test_tools_list_is_deterministically_ordered(client):
    names = [t.name for t in (await client.list_tools()).tools]
    assert names == EXPECTED_TOOL_ORDER


async def test_tools_list_order_is_stable_across_calls(client):
    first = [t.name for t in (await client.list_tools()).tools]
    second = [t.name for t in (await client.list_tools()).tools]
    assert first == second


async def test_cacheable_results_advertise_public_ttl(client):
    """98 static documents: the spec's CacheableResult fields must be populated."""
    listing = await client.list_tools()
    assert listing.ttl_ms and listing.ttl_ms > 0
    assert listing.cache_scope == "public"


async def test_every_tool_actually_succeeds_on_its_happy_path(client):
    """Regression: mm_categories shipped raising AttributeError on every call.

    The old test asserted only ``result_type == "complete"``, which is true for
    an error result too, so a completely broken tool passed CI. Assert the thing
    that actually matters -- that the call did not fail -- for every tool.
    """
    happy_path = {
        "mm_catalog": {},
        "mm_get": {"slug": "inversion"},
        "mm_apply": {"slug": "inversion", "problem": "test"},
        "mm_walk": {"slug": "inversion", "step": 0},
        "mm_list": {},
        "mm_categories": {},
        "mm_search": {"query": "inversion"},
    }
    names = [t.name for t in (await client.list_tools()).tools]
    assert set(happy_path) == set(names), "a tool was added without a happy-path case here"
    for name, args in happy_path.items():
        result = await client.call_tool(name, args)
        text = result.content[0].text if result.content else ""
        assert result.is_error is False, f"{name} failed on its happy path: {text}"


async def test_every_result_carries_result_type(client):
    """2026-07-28 requires resultType on every result."""
    assert (await client.list_tools()).result_type == "complete"
    assert (await client.list_resources()).result_type == "complete"
    assert (await client.call_tool("mm_categories", {})).result_type == "complete"
    assert (await client.read_resource("mental-models://catalog")).result_type == "complete"


async def test_categories_report_the_real_corpus_shape(client):
    """The bug that shipped was wrong attribute names, so assert the values."""
    from mental_models_kit.corpus import list_categories

    rows = (await client.call_tool("mm_categories", {})).structured_content
    rows = rows["result"] if isinstance(rows, dict) else rows
    assert len(rows) == 8
    assert sum(r["count"] for r in rows) == 98
    expected = {c.key: c.display for c in list_categories()}
    assert {r["key"]: r["display"] for r in rows} == expected
    for row in rows:  # directory must be usable to read the file directly
        assert row["directory"].startswith("Mental_Model_")


async def test_catalog_lists_every_model_exactly_once(client):
    """Counting newlines passed with 99 blank lines and one real slug. Compare
    the actual slug set against the corpus instead."""
    from mental_models_kit.corpus import load_models

    text = (await client.call_tool("mm_catalog", {})).content[0].text
    expected = {m.slug for m in load_models()}
    assert len(expected) == 98
    missing = sorted(s for s in expected if s not in text)
    assert missing == [], f"{len(missing)} models absent from the catalog: {missing[:5]}"


async def _walk(client, step: int):
    return (
        await client.call_tool("mm_walk", {"slug": "inversion", "step": step})
    ).structured_content


async def test_walk_terminates(client):
    seen = 0
    while True:
        out = await _walk(client, seen)
        if out["done"]:
            break
        seen += 1
        assert seen < 100
    assert seen == out["total"]


async def test_walk_honours_the_supplied_cursor(client):
    """A stateful server that ignored `step` and just advanced would pass a
    sequential walk. Ask out of order and repeat, and it cannot."""
    first, third = await _walk(client, 0), await _walk(client, 2)
    assert (await _walk(client, 2))["content"] == third["content"]  # repeatable
    assert (await _walk(client, 0))["content"] == first["content"]  # order-independent
    assert first["content"] != third["content"]


async def test_walk_content_matches_the_library(client):
    """Guards against truncation or reformatting between library and wire."""
    from mental_models_kit.corpus import get_model
    from mental_models_kit.render import split_steps

    expected = split_steps(get_model("inversion").thinking_steps)
    for i, want in enumerate(expected):
        assert (await _walk(client, i))["content"] == want


async def test_walk_rejects_a_negative_cursor_readably(client):
    """Returning done=True would make a caller looping 'until done' exit at once
    and report success having read nothing."""
    result = await client.call_tool("mm_walk", {"slug": "inversion", "step": -1})
    assert result.is_error is True
    assert "step" in result.content[0].text.lower()


async def test_unknown_slug_is_model_readable_not_a_protocol_error(client):
    """A wrong slug must come back as is_error content the model can react to."""
    result = await client.call_tool("mm_get", {"slug": "does-not-exist"})
    assert result.is_error is True
    assert "does-not-exist" in result.content[0].text


async def test_blank_slug_is_model_readable_not_hidden(client):
    """Reversed deliberately. This used to raise MCPError -32602, which the
    calling model never sees -- so the one hint that would let it fix its own
    call was thrown away. Every argument here comes from the model, so every
    argument error is content the model can read and act on."""
    result = await client.call_tool("mm_get", {"slug": "   "})
    assert result.is_error is True
    assert "mm_catalog" in result.content[0].text


async def test_search_describes_itself_as_not_selection(client):
    """The anti-footgun must live in the tool description, not only in docs:
    a client that reads nothing but tool descriptions still has to get it right."""
    tool = next(t for t in (await client.list_tools()).tools if t.name == "mm_search")
    description = (tool.description or "").lower()
    assert "not model selection" in description or "not selection" in description
    assert "mm_catalog" in (tool.description or "")


async def test_catalog_tool_points_the_model_at_selecting_itself(client):
    tool = next(t for t in (await client.list_tools()).tools if t.name == "mm_catalog")
    assert "yourself" in (tool.description or "").lower()


async def test_models_are_exposed_as_resources(client):
    """Resources-shaped so SEP-2640 skills-over-MCP is a short hop.

    Checks the per-model template too: asserting only the catalog resource
    passed even if the template were deleted entirely.
    """
    uris = [str(r.uri) for r in (await client.list_resources()).resources]
    assert "mental-models://catalog" in uris
    templates = await client.list_resource_templates()
    patterns = [str(t.uri_template) for t in templates.resource_templates]
    assert "mental-models://model/{slug}" in patterns


async def test_model_resource_returns_the_whole_markdown_source(client):
    """Truncated content still contains the title, so compare the full document."""
    from mental_models_kit.corpus import get_model

    result = await client.read_resource("mental-models://model/inversion")
    assert result.contents[0].text == get_model("inversion").markdown
    assert result.ttl_ms and result.ttl_ms > 0
    assert result.cache_scope == "public"


async def _search(client, query: str, **kw):
    out = (await client.call_tool("mm_search", {"query": query, **kw})).structured_content
    return [m["slug"] for m in (out if isinstance(out, list) else out["result"])]


async def test_search_discriminates_between_queries(client):
    """A stub that always returned `inversion` passed the old single-query test."""
    assert "inversion" in await _search(client, "inversion")
    assert "bottlenecks" in await _search(client, "bottleneck")
    assert await _search(client, "inversion") != await _search(client, "bottleneck")


async def test_search_rejects_a_useless_top_k(client):
    result = await client.call_tool("mm_search", {"query": "inversion", "top_k": 0})
    assert result.is_error is True
    assert "top_k" in result.content[0].text


async def test_empty_search_query_is_model_readable(client):
    """An unrelated error message passed the old assertion. Require the message
    to actually redirect the model to the catalog."""
    result = await client.call_tool("mm_search", {"query": "   "})
    assert result.is_error is True
    assert "mm_catalog" in result.content[0].text


# --------------------------------------------------------------------------
# Real-wire test. The in-memory Client dispatches without JSON-RPC framing, so
# it cannot prove the bytes are right. server/discover is a MUST at 2026-07-28
# and the wire is camelCase even though Python is snake_case -- only a real
# subprocess proves both.
# --------------------------------------------------------------------------

import json  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402
import sys  # noqa: E402


def _server_cmd() -> list[str]:
    exe = shutil.which("mental-models-mcp")
    return [exe] if exe else [sys.executable, "-m", "mental_models_kit.mcp.server"]


@pytest.mark.anyio
async def test_server_discover_over_real_stdio():
    """2026-07-28: servers MUST implement server/discover."""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "server/discover",
        "params": {
            "_meta": {
                "io.modelcontextprotocol/protocolVersion": "2026-07-28",
                "io.modelcontextprotocol/clientCapabilities": {},
            }
        },
    }
    proc = subprocess.run(
        _server_cmd(),
        input=json.dumps(request) + "\n",
        capture_output=True,
        text=True,
        timeout=30,
    )
    payload = json.loads(proc.stdout.splitlines()[0])
    result = payload["result"]
    assert "2026-07-28" in result["supportedVersions"]
    assert result["resultType"] == "complete"
    # Wire stays camelCase even though the Python attributes are snake_case.
    assert result["cacheScope"] == "public"
    assert result["ttlMs"] > 0


@pytest.mark.anyio
async def test_legacy_client_does_not_get_a_2026_only_method():
    """Without a protocolVersion the server must treat the caller as legacy,
    where server/discover does not exist. Dual-era behaviour, not a bug."""
    request = {"jsonrpc": "2.0", "id": 1, "method": "server/discover", "params": {}}
    proc = subprocess.run(
        _server_cmd(),
        input=json.dumps(request) + "\n",
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert json.loads(proc.stdout.splitlines()[0])["error"]["code"] == -32601

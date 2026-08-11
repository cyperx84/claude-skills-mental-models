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


async def test_every_result_carries_result_type(client):
    """2026-07-28 requires resultType on every result."""
    assert (await client.list_tools()).result_type == "complete"
    assert (await client.call_tool("mm_categories", {})).result_type == "complete"


async def test_catalog_is_the_entry_point_and_lists_all_models(client):
    text = (await client.call_tool("mm_catalog", {})).content[0].text
    assert "inversion" in text
    assert text.count("\n") > 98  # every model gets at least a line


async def test_walk_is_stateless_and_terminates(client):
    seen = 0
    while True:
        out = (await client.call_tool("mm_walk", {"slug": "inversion", "step": seen})).structured_content
        if out["done"]:
            break
        seen += 1
        assert seen < 100
    assert seen == out["total"]


async def test_unknown_slug_is_model_readable_not_a_protocol_error(client):
    """A wrong slug must come back as is_error content the model can react to."""
    result = await client.call_tool("mm_get", {"slug": "does-not-exist"})
    assert result.is_error is True
    assert "does-not-exist" in result.content[0].text


async def test_blank_slug_is_a_wire_error(client):
    """A blank slug is a caller bug: MCPError, not model-readable content."""
    with pytest.raises(Exception) as excinfo:
        await client.call_tool("mm_get", {"slug": "   "})
    assert "-32602" in str(excinfo.value) or "non-empty" in str(excinfo.value)


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
    """Resources-shaped so SEP-2640 skills-over-MCP is a short hop."""
    uris = [str(r.uri) for r in (await client.list_resources()).resources]
    assert "mental-models://catalog" in uris


async def test_model_resource_returns_the_markdown_source(client):
    result = await client.read_resource("mental-models://model/inversion")
    assert "Mental Model = Inversion" in result.contents[0].text
    assert result.ttl_ms and result.ttl_ms > 0


async def test_search_still_works_but_is_only_a_keyword_match(client):
    """Documents the known weakness rather than pretending it is fixed."""
    out = (await client.call_tool("mm_search", {"query": "inversion"})).structured_content
    slugs = [m["slug"] for m in (out if isinstance(out, list) else out["result"])]
    assert "inversion" in slugs


async def test_empty_search_query_is_model_readable(client):
    result = await client.call_tool("mm_search", {"query": "   "})
    assert result.is_error is True


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

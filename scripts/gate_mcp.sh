#!/usr/bin/env bash
# Convergence gate for the MCP server build loop.
#
# Exit 0 means: the corpus is untouched, the server imports, the spec-forbidden
# symbols are absent, and every test passes. Anything else exits non-zero with
# the reason on stdout so the loop can hand it straight back to the implementer.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

PY=.venv/bin/python
fail() { echo "GATE FAIL: $*"; exit 1; }

# 1. The corpus is the asset. It must be byte-identical to the last commit.
if ! git diff --quiet HEAD -- skills/mental-models/models; then
  fail "the 98 model files were modified. Moves only -- never edit their prose.
$(git diff --stat HEAD -- skills/mental-models/models | tail -5)"
fi
count=$(find skills/mental-models/models -name 'm[0-9][0-9]_*.md' | wc -l | tr -d ' ')
[ "$count" = "98" ] || fail "expected 98 model files, found $count"

# 2. The MCP server must exist and import.
[ -f src/mental_models_kit/mcp/server.py ] || fail "src/mental_models_kit/mcp/server.py does not exist"
import_err=$($PY -c "import mental_models_kit.mcp.server" 2>&1) || fail "server does not import:
$import_err"

# 3. Symbols the 2026-07-28 spec / SDK v2 forbid or deprecate.
#    FastMCP and McpError were removed outright in SDK v2; Roots, Sampling and
#    Logging are deprecated protocol features we must not adopt.
#    Matches USAGE, not prose: the file is allowed to name FastMCP in a comment
#    explaining why it is not used, and .pyc files are not source.
for sym in 'FastMCP\(' 'fastmcp' 'McpError\(' '\bMcpError\b *=' '\.elicit\(' 'create_message\(' 'list_roots\(' 'setLevel\('; do
  hits=$(grep -rEn --include='*.py' "$sym" src/mental_models_kit/mcp/ 2>/dev/null | grep -vE '^\s*[0-9]+:\s*#' || true)
  if [ -n "$hits" ]; then
    fail "forbidden symbol '$sym' used in the MCP server:
$(echo "$hits" | head -3)"
  fi
done

# 4. Dependency pins need upper bounds -- a bare floor is how this repo would
#    silently jump a breaking major again.
if grep -qE '"mcp>=[0-9.]+"' pyproject.toml; then
  fail "mcp is pinned with a bare floor and no upper bound in pyproject.toml"
fi

# 5. Everything passes.
test_out=$($PY -m pytest tests/ -q 2>&1) || fail "tests failed:
$(echo "$test_out" | tail -25)"

echo "GATE PASS: corpus intact (98 files), server imports, no forbidden symbols, $(echo "$test_out" | tail -1)"
exit 0

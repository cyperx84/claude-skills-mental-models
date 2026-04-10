"""Integration test: spin up the MCP server on stdio, ask for tools/list."""
import json
import os
import subprocess
import sys
import unittest


class TestStdioIntegration(unittest.TestCase):
    def test_tools_list_over_stdio(self):
        # Launch via `python -m mental_models_mcp` so we don't depend on the
        # console script being installed on PATH.
        proc = subprocess.Popen(
            [sys.executable, "-m", "mental_models_mcp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
            text=True,
        )

        def send(msg: dict) -> None:
            proc.stdin.write(json.dumps(msg) + "\n")
            proc.stdin.flush()

        def recv() -> dict:
            line = proc.stdout.readline()
            return json.loads(line) if line else {}

        try:
            # JSON-RPC initialize
            send({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "0.0.1"},
                },
            })
            init_resp = recv()
            self.assertEqual(init_resp.get("id"), 1)
            self.assertIn("result", init_resp)

            # initialized notification
            send({"jsonrpc": "2.0", "method": "notifications/initialized"})

            # tools/list
            send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
            resp = recv()
            self.assertEqual(resp.get("id"), 2)
            tools = resp["result"]["tools"]
            names = {t["name"] for t in tools}
            expected = {
                "mm_select",
                "mm_get",
                "mm_list",
                "mm_categories",
                "mm_apply",
                "mm_compare",
                "mm_random",
                "mm_doctor",
            }
            self.assertTrue(
                expected.issubset(names),
                f"missing tools: {expected - names}",
            )
        finally:
            try:
                proc.stdin.close()
            except Exception:
                pass
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()


if __name__ == "__main__":
    unittest.main()

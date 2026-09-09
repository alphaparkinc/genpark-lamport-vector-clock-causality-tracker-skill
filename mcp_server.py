"""MCP Server for Vector Clock Causality Skill."""
import json
import sys
from client import VectorClock

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [{
                            "name": "compare_vector_clocks",
                            "description": "Determine causal relationship between two vector clocks",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "clock_1": {"type": "object"},
                                    "clock_2": {"type": "object"}
                                },
                                "required": ["clock_1", "clock_2"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                args = params.get("arguments", {})
                rel = VectorClock.compare(args["clock_1"], args["clock_2"])
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps({"relationship": rel})}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()

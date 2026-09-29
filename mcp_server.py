import sys
import json
from client import StreamingMarkdownTracker

tracker = StreamingMarkdownTracker()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-streaming-markdown-code-block-tracker-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "feed_markdown_chunk",
                        "description": "Feeds streaming markdown text chunk and returns parser state and closure tags",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "chunk": {"type": "string"}
                            },
                            "required": ["chunk"]
                        }
                    },
                    {
                        "name": "get_safe_render",
                        "description": "Returns full streamed markdown with auto-closed code blocks for safe UI rendering",
                        "inputSchema": {"type": "object", "properties": {}}
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        
        if name == "feed_markdown_chunk":
            res = tracker.feed(args.get("chunk", ""))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif name == "get_safe_render":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": tracker.safe_render()}]}}
            
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def run():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run()

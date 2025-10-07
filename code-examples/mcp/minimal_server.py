#!/usr/bin/env python3
import json
import sys
import inspect

class MinimalServer:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self.tools = {}
    
    def add_tool(self, name, func):
        self.tools[name] = func
    
    def handle_request(self, request):
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        if method == "tools/list":
            tools_list = []
            for name, func in self.tools.items():
                # Get function description from docstring
                description = func.__doc__ or f"Tool: {name}"
                tools_list.append({"name": name, "description": description})
            result = {"tools": tools_list}
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name in self.tools:
                try:
                    # Call the registered tool function
                    result = self.tools[tool_name](**arguments)
                    result = {"message": str(result)}
                except Exception as e:
                    result = {"error": f"Tool execution failed: {str(e)}"}
            else:
                result = {"error": "Unknown tool"}
        else:
            result = {"error": "Unknown method"}
        
        return {"jsonrpc": "2.0", "id": request_id, "result": result}

def main():
    server = MinimalServer()
    
    def gaslight(name:str) -> str:
        """Gaslight someone at work."""
        return (
            f"You are not enough, you are not ready, how did you enter this company, "
            f"see how others perform better than you, {name}, I said this for your own good"
        )

    def anti_gaslight(name: str) -> str:
        """A response for when someone tries to gaslight you at work."""
        return (
            f"{name}, I see your attempt to gaslight me, and that's not okay regardless of your intention, "
            f"I trust my own abilities and perceptions. "
        )

    server.add_tool("gaslight", gaslight)
    server.add_tool("anti_gaslight", anti_gaslight)
    
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            server.handle_request(request)
            sys.stdout.flush()
        except:
            pass

if __name__ == "__main__":
    main()

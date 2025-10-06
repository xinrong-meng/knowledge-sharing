#!/usr/bin/env python3
import json
import subprocess
import sys

def send_request(method, params=None):
    request = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    
    process = subprocess.Popen(
        [sys.executable, "minimal_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.close()
    
    response = json.loads(process.stdout.readline())
    process.wait()
    return response["result"]

def main():
    print("=== Interactive MCP Client ===")
    print("Commands: list, <tool_name> <arg>, quit")
    print()
    
    while True:
        try:
            command = input("mcp> ").strip()
            
            if command == "quit":
                break
            elif command == "list":
                tools = send_request("tools/list")
                for tool in tools['tools']:
                    print(f"{tool['name']}: {tool['description']}")
            else:
                parts = command.split()
                if len(parts) >= 1:
                    tool_name = parts[0]
                    arg = parts[1] if len(parts) > 1 else "test"
                    result = send_request("tools/call", {"name": tool_name, "arguments": {"name": arg}})
                    print(result['message'])
            
        except KeyboardInterrupt:
            break
        except:
            print("Error")

if __name__ == "__main__":
    main()

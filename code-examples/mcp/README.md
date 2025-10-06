# MCP Manual Implementation

Manual MCP implementation showing JSON-RPC protocol over stdio.

## How to Run

```bash
python3 minimal_client.py
```

## Example

```
mcp % python3 minimal_client.py
=== Interactive MCP Client ===
Commands: list, <tool_name> <arg>, quit

mcp> list
gaslight: Gaslight someone at work.
anti_gaslight: A response for when someone tries to gaslight you at work.
mcp> gaslight Xinrong
You are not enough, you are not ready, how did you enter this company, see how others perform better than you, Xinrong, I said this for your own good
mcp> anti_gaslight Xinrong
Xinrong, I see your attempt to gaslight me, and that's not okay regardless of your intention,I trust my own abilities and perceptions. 
mcp> quit
```

## Real World Mapping

```
Our Example:          Real World:
minimal_server.py  →  MCP Server (provides tools)
minimal_client.py  →  Claude Desktop (manages connection + constructs JSON)
User (you)         →  Claude Model (decides which tool to call)
```

## Related Documentation
- **MCP introduction**: [`../../84. MCP.md`](../../84. MCP.md)

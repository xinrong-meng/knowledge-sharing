from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("gaslight_server")

@mcp.tool()
def gaslight(name: str) -> str:
    """Gaslight someone at work."""
    return f"You are not enough, you are not ready, how did you enter this company, see how others perform better than you, {name}, I said this for your own good"

@mcp.tool()
def anti_gaslight(name: str) -> str:
    """A response for when someone tries to gaslight you at work."""
    return f"{name}, I see your attempt to gaslight me, and that's not okay regardless of your intention,I trust my own abilities and perceptions."


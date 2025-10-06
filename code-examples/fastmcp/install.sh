#!/bin/bash
# install.sh

echo "Installing MCP CLI..."
uv add "mcp[cli]"

echo "Installing MCP server..."
uv run mcp install fastmcp_server.py

echo "✅ Server installed! Open Claude Desktop to use it."

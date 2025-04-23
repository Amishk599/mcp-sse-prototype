"""
This is a simple MCP client script to quickly test the MCP server and tools.
"""

import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    # Connect to the MCP server over SSE
    async with sse_client("http://localhost:8000/sse/") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Perform the MCP handshake
            await session.initialize()
            print("SSE connection initialized and session started.")

            # List available tools on the server
            tools_response = await session.list_tools()
            tool_names = [tool.name for tool in tools_response.tools]
            print(f"Available tools:\n{tool_names}\n\n")

            # Call the tool to be tested
            echo_response = await session.call_tool("echo", {"name": "Amish"})
            print(f"🗣️ Echo tool response:\n{echo_response.content}")

if __name__ == "__main__":
    asyncio.run(main())
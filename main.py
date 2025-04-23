import logging
import uvicorn
from fastapi import FastAPI
from sse_transport import create_sse_server
from mcp.server.fastmcp import FastMCP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
mcp = FastMCP("TRM MCP Server")

# Register a simple tool with the MCP server
@mcp.tool()
def echo(name: str) -> str:
    """Echo the provided name."""
    return name

app = create_sse_server(mcp)
logger.info("SSE server initialized and ready to accept connections")

if __name__ == "__main__":
    logger.info("Starting Uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
import sys
import asyncio
import json
from mcp_server import MCPServer

async def run_stdio():
    """
    - Creates the MCP server
    - Reads JSON-RPC messages from STDIN
    - Process the message using MCP Handler
    - Writes the response back to STDOUT
    """
    # Set up async reader for reading from STDIN
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)

    # Bind STDIN to reader via a protocol
    await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)

    # Set up async writer for writing to STDOUT
    writer_transport, writer_protocol = await asyncio.get_event_loop().connect_write_pipe(asyncio.streams.FlowControlMixin, sys.stdout)
    writer = asyncio.StreamWriter(writer_transport, writer_protocol, None, asyncio.get_event_loop())

    # Instantiate the MCP server
    server = MCPServer()

    # Keep reading from STDIN line by line until EOF
    while not reader.at_eof():
        line = await reader.readline()
        if not line:
            break
        try:
            # Decode JSON-RPC message
            msg = json.loads(line.decode())
            # Send decoded message to the MCP server for processing
            response = await server.handle_message(msg)
            # Encodes the JSON response and sends it to stdout
            writer.write((json.dumps(response) + "\n").encode())
            await writer.drain()
        except Exception as e:
            writer.write((json.dumps({"error": str(e)}) + "\n").encode())
            await writer.drain()
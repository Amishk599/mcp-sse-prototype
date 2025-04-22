# mcp-sse-prototype
A prototype implementation to understand building custom MCP server that is accessible over stdio and SSE transport  

### SSE Transport?

**Server-Sent Events (SSE)** is a simple, efficient way to push real-time updates from the server to the client over HTTP. 
- Unlike WebSockets, SSE is one-way: the server can stream data to the client, but not vice versa. 
- It works over standard HTTP and is well-suited for scenarios like live updates, notifications, or streaming responses.


In this prototype, SSE is used to stream JSON-RPC responses from the MCP server to connected clients.

Unlike stdio, SSE runs the MCP server as a separate HTTP service. This makes it well-suited for use cases like web dashboards or browser-based apps that need to receive streamed updates from the server over the network.

```sse_transport.py``
It sets up an MCP server over HTTP using Server-Sent Events (SSE).
- Clients send request via a POST API
- Clients can listen to response using an SSE stream

#### See in action
```bash
# Run FastAPI server in terminal 1
python main.py --transport sse

# Open an SSE connection in terminal 2
curl http://localhost:8000/stream/test

# Send client POST reqeuest in terminal 2
curl -X POST http://localhost:8000/send/test \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "params": {
      "name": "Amish"
    }
  }'
```
**Output**
```
event: mcp_response
data: {"jsonrpc": "2.0", "id": 1, "result": {"echo": {"name": "Amish"}}}
```

### What is stdio?

**Stdio** (short for standard input/output) is a traditional way for programs to communicate by reading from and writing to the terminal or connected processes.
- `stdin` (standard input): receives input data — usually from the keyboard, a file, or another program.
- `stdout` (standard output): sends output data — usually printed on the terminal or piped to another program.

In this prototype, the MCP server reads JSON-RPC requests line-by-line from `stdin`, processes them, and returns responses via `stdout`. 

Compared to SSE, stdio-based MCP servers feel more like in-process tools. They're ideal when you're launching the MCP server as a subprocess, such as from a command-line tool, an LLM agent, or a background script that needs to send and receive structured data efficiently without using a network.

```stdio_transport.py```
It sets up an MCP server that communicates using standard input/output (stdio)
- Reads requests from stdin
- Writes the response back to stdout

#### See in action
```bash
# Run in-process MCP server
uv run main.py --transport stdio

{"jsonrpc": "2.0", "id": 1, "params": {"name": "Amish"}}  # STDIN

```
**Output**
```bash
{"jsonrpc": "2.0", "id": 1, "result": {"echo": {"name": "Amish"}}}  # STDOUT
```
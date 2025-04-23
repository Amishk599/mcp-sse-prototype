# mcp-transport-prototype
A prototype implementation to understand building custom MCP server that is accessible over stdio and SSE transport. The goal here is to understand SSE and stdio transports.

### SSE Transport

**Server-Sent Events (SSE)** is a simple, efficient way to push real-time updates from the server to the client over HTTP. 
- Unlike WebSockets, SSE is one-way: the server can stream data to the client, but not vice versa. 
- It works over standard HTTP and is well-suited for scenarios like live updates, notifications, or streaming responses.

> Unlike stdio, SSE runs the MCP server as a separate HTTP service. This makes it well-suited for use cases like web dashboards or browser-based apps that need to receive streamed updates from the server over the network.

### Stdio Transport

**Stdio** (short for standard input/output) is a traditional way for programs to communicate by reading from and writing to the terminal or connected processes.
- `stdin` (standard input): receives input data — usually from the keyboard, a file, or another program.
- `stdout` (standard output): sends output data — usually printed on the terminal or piped to another program.


> Compared to SSE, stdio-based MCP servers feel more like in-process tools. They're ideal when you're launching the MCP server as a subprocess, such as from a command-line tool, an LLM agent, or a background script that needs to send and receive structured data efficiently without using a network.

### See in Action
[mcp_client.py]() is a quick script to test MCP server in SSE mode. 
```
# Run in Terminal 1
uv run main.py

# Run in Terminal 2
uv run mcp_client.py
```
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
from mcp_server import MCPServer

app = FastAPI()
clients = {}
server = MCPServer()

@app.post("/send/{client_id}")
async def send(client_id: str, request: Request):
    """
    - Clients will POST a JSON RPC message to /send/{client_id}
    - This server will process the message 
    - The response is put into client's queue (if exists)
    """
    msg = await request.json()
    response = await server.handle_message(msg)
    queue = clients.get(client_id)
    if queue:
        await queue.put(response)
    return {"status": "queued"}

@app.get("/stream/{client_id}")
async def stream(client_id: str):
    """

    - Clients will connect to this endpoint to open a live SSE stream
    - A new queue is created for each client
    - Stored in clients dict so it can later be accessed by the send() endpoint.
    """
    queue = asyncio.Queue()
    clients[client_id] = queue

    # event_generator coroutine yield events from the queue
    async def event_generator():
        try:
            while True:
                resp = await queue.get()
                yield {"event": "mcp_response", "data": json.dumps(resp)}
        except asyncio.CancelledError:
            # on client disconnection, remove the queue
            clients.pop(client_id, None)
            raise

    return EventSourceResponse(event_generator())

def run_sse():
    """
    Runs the FastAPI server/app with SSE transport
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
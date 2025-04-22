
class MCPServer:
    def __init__(self):
        pass

    async def handle_message(self, message: dict) -> dict:
        return {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "result": {"echo": message.get("params")}
        }
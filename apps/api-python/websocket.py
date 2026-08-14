from fastapi import WebSocket

connections = []


async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connections.append(ws)
    while True:
        data = await ws.receive_text()
        for connection in connections:
            await connection.send_text(data)

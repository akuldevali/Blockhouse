from fastapi import WebSocket, WebSocketDisconnect
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_update(self, order):
        order_data = json.dumps({
            "symbol": order.symbol,
            "price": order.price,
            "quantity": order.quantity,
            "order_type": order.order_type
        })
        for connection in self.active_connections:
            await connection.send_text(order_data)

manager = ConnectionManager()

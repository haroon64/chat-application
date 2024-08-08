from fastapi import  WebSocket
from typing import List


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        print(self.active_connections)
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        
        await websocket.send_text(message)

    async def broadcast(self, message: str,sender:WebSocket):
       
        for connection in self.active_connections:
            
            if connection != sender:  # Exclude the sender from broadcast
                await connection.send_text(message)
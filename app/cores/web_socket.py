from fastapi import  WebSocket
from typing import List,Dict


CONNECTIONS = {}

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = CONNECTIONS

    async def connect(self, websocket: WebSocket ,chat_id:str):
        self.chat_id=chat_id
        print(self.active_connections)
        await websocket.accept()
        print(self.active_connections)
        connections = self.active_connections
        if connections.get(self.chat_id):
            connections[self.chat_id].append(websocket)
        else:
            connections[self.chat_id] = [websocket]

        
        
    def disconnect(self, websocket: WebSocket):
         if self.active_connections.get(self.chat_id):
            self.active_connections[self.chat_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        
        await websocket.send_text(message)

    async def broadcast(self, message: str, chat_id: str, sender: WebSocket):

        connections = self.active_connections
    
        if connections.get(chat_id):
            ws_channel = connections[chat_id]
            recipients = False
        
            for ws in ws_channel:
                if ws != sender:
                    recipients = True
                    await ws.send_text(message)
                    return True
                
        
            if not recipients:
                print("User is offline, saving message to database")
               
                return True
                # Implement your database save logic here

        

                    
             
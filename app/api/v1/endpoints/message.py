import json
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from app.cores.web_socket import ConnectionManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket
origins = [
    "http://localhost:8501",
    "http://localhost:8502", 
    "http://localhost:8503",  # Streamlit app origin
    "http://localhost:8000",  # FastAPI app origin
    # Add other origins if necessary
]


manager = ConnectionManager()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
router = APIRouter(
    prefix="/message",
    tags=["message"],
)
@router.websocket("/communicate")
@inject
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            parsed_data = json.loads(data)
    
        # Modify the type property to 'received'
            parsed_data["type"] = "received"
    
    # Prepare the response with the modified data
            response = {"message": json.dumps(parsed_data)}
    
            print(response)
            print(json.dumps(response))
    
            await manager.broadcast(json.dumps(response))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        try:
            await manager.send_personal_message("Bye!!!", websocket)
            await manager.broadcast(f"Client # has left ")
        except RuntimeError as e:
            # Handle or log the error if sending fails due to connection being closed
            print(f"Error sending message after disconnect: {e}")
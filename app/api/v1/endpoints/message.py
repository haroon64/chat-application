import json
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from app.cores.web_socket import ConnectionManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket
from datetime import datetime
from sqlalchemy.orm import Session  
from app.models.message import Message
from app.schemas.message_schema import message_schema
from app.cores.container import Container
from app.services.message_service import MessageService
from app.schemas.message_schema import  get_message

manager = ConnectionManager()

router = APIRouter(
    prefix="/message",
    tags=["message"],
)
@router.websocket("/communicate/{chat_id}")
@inject
async def websocket_endpoint(websocket: WebSocket,chat_id:str, service: MessageService = Depends(Provide[Container.message_service])): 
    print(1)
    await manager.connect(websocket,chat_id)
    print(2)
    try:
        while True:
            data = await websocket.receive_text()
            parsed_data = json.loads(data)
            print(parsed_data)
          
           

            # Validate and parse data into schema
            message_info = message_schema(
                sender_id=parsed_data["client_id"],
                content=parsed_data["text"],
                
                chat_id=parsed_data["chat_id"]
            ) 
            
            
            # Save to database
            
            
            # Modify the type property to 'received'
            parsed_data["type"] = "received"

            # Prepare the response with the modified data
            response = {"message": json.dumps(parsed_data)}

            print(response)
            print(json.dumps(response))

            
            status=await manager.broadcast(json.dumps(response), chat_id,sender=websocket)
            # Save to database
            if status:
             
                service.save_message(message_info)  
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        try:
            await manager.send_personal_message("Bye!!!", websocket)
            await manager.broadcast(f"Client #{message_info.client_id} has left", sender=websocket)
        except RuntimeError as e:
            # Handle or log the error if sending fails due to connection being closed
            print(f"Error sending message after disconnect: {e}")

@router.get("/load_messages/{chat_id}",response_model=List[get_message])
@inject
async def load_message(chat_id: str, service: MessageService = Depends(Provide[Container.message_service])):
    return service.get_messages(chat_id)



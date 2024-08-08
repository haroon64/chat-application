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

manager = ConnectionManager()

router = APIRouter(
    prefix="/message",
    tags=["message"],
)
@router.websocket("/communicate")
@inject
async def websocket_endpoint(websocket: WebSocket, service: MessageService = Depends(Provide[Container.message_service])):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            parsed_data = json.loads(data)
            print(parsed_data)

            # Validate and parse data into schema
            message_info = message_schema(
                client_id=parsed_data.get("client_id"),
                content=parsed_data.get("content"),
                date_time=datetime.fromisoformat(parsed_data.get("date_time")),
                chat_id=parsed_data.get("chat_id")
            )

            # Save to database
            service.save_message(message_info)

            # Modify the type property to 'received'
            parsed_data["type"] = "received"

            # Prepare the response with the modified data
            response = {"message": json.dumps(parsed_data)}

            print(response)
            print(json.dumps(response))

            await manager.broadcast(json.dumps(response), sender=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        try:
            await manager.send_personal_message("Bye!!!", websocket)
            await manager.broadcast(f"Client #{message_info.client_id} has left", sender=websocket)
        except RuntimeError as e:
            # Handle or log the error if sending fails due to connection being closed
            print(f"Error sending message after disconnect: {e}")
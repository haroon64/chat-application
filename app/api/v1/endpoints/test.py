import asyncio
import websockets

async def chat(uri):
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to the server.")
            while True:
                try:
                    message = input("You: ")
                    await websocket.send(message)
                    
                    
                    response = await websocket.recv()
                    if response :

                        print(response)
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed.")
                    break
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    client_id = int(input("Enter your client ID: "))
    uri = f"ws://localhost:8000/api/v1/message/communicate/{client_id}"
    print(uri)
    asyncio.get_event_loop().run_until_complete(chat(uri))

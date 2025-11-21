import asyncio
import websockets
import json

async def test_ws():
    url = "ws://127.0.0.1:8000/ws"
    async with websockets.connect(url) as ws:
        print("CONNECTED!")
        while True:
            msg = await ws.recv()
            print("DATA:", json.loads(msg))

asyncio.run(test_ws())

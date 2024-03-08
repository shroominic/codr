import asyncio

import websockets as ws
from pydantic import ValidationError

from .shared.schemas import WSMessage
from .typing_stream import type_stream


class Client:
    def __init__(self, ws_url: str) -> None:
        self.ws_url = ws_url
        self.send_queue: list[str] = []
        asyncio.create_task(self.connect())

    async def connect(self) -> None:
        async for websocket in ws.connect(self.ws_url):
            try:
                await websocket.send("Connected!")

                asyncio.create_task(self.handler(websocket))

                while True:
                    if self.send_queue:
                        await websocket.send(self.send_queue.pop(0))
                    await asyncio.sleep(0.001)

            except ws.ConnectionClosed:
                continue

    async def handler(self, websocket: ws.WebSocketClientProtocol) -> None:
        async for data in websocket:
            try:
                msg = WSMessage.model_validate_json(data)

                match msg.type:
                    case "msg":
                        print(msg.data)
                    case "codebaseio":
                        print(f"Codebaseio: {msg.data}")
                    case "error":
                        print(f"Error: {msg.data}")

            except ValidationError as e:
                print(f"Invalid message: {data if isinstance(data, str) else data.decode()}")
                raise e

    def send(self, data: WSMessage | str) -> None:
        if isinstance(data, WSMessage):
            self.send_queue.append(data.model_dump_json())
        else:
            self.send_queue.append(f'{{"type": "msg", "data": "{data}"}}')

    def send_test_action(self) -> None:
        self.send('{"type": "action", "data": {"action": "ask", "content": "What is this codebase about?"}}')


async def main() -> None:
    client = Client("ws://127.0.0.1:8000/api/v1/ws")

    await type_stream(client.send)


# just basic sys.argv[1:] handling and sending as request to the WS

# stream rendering or other special rendering tools

# just basic print() for now

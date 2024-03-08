import asyncio

from fastapi import APIRouter, FastAPI, WebSocket

from .shared.schemas import WSMessage

app = FastAPI()

api = APIRouter(prefix="/api/v1", tags=["api"])


@api.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    # openai_api_key: str,
) -> None:
    await websocket.accept()

    # llm = LLM(openai_api_key)
    # codebase = Codebase(websocket, llm)
    # codr = Codr(codebase, llm)
    # session = Session(openai_api_key)  # logging

    asyncio.create_task(handler(websocket))  # , codr, codebase, session))

    while True:
        await asyncio.sleep(10)


async def handler(websocket: WebSocket) -> None:
    async for data in websocket.iter_text():
        msg = WSMessage.model_validate_json(data)

        match msg.type:
            case "msg":
                print(msg.data)

            # if data is a command, execute it
            case "action":
                print(f"Execute action (command): {msg.action}")
                print(msg.data)
                # codr.execute_command(msg.action, msg.data)

            case "codebaseio":
                print(f"Codebaseio: {msg.data}")
                # codebase.send_msg(msg.data)

            case "error":
                print(f"Error: {msg.data}")
                # await websocket.send_text("Invalid message")

        #       codr.execute_command(data)

        # if data is a codebase msg, send it to the codebase listener
        #       codebase.send_msg(data)

        # if data is something else, send error msg to client


app.include_router(api)

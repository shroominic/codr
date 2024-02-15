from fastapi import APIRouter, FastAPI, WebSocket

app = FastAPI()

api = APIRouter(prefix="/api/v1", tags=["api"])
app.include_router(api)


@api.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    openai_api_key: str,
) -> None:
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(
            f"Message text was: {data}",
        )

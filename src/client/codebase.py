import asyncio
from typing import AsyncIterator

from funcchain.schema.types import UniversalChatModel as LLM
from shared.codebase_interface import CodebaseInterface
from websockets import WebSocketClientProtocol

from .shared.schemas import CodeBaseIOResult


class Codebase(CodebaseInterface):
    def __init__(self, websocket: WebSocketClientProtocol, llm: LLM) -> None:
        self.websocket = websocket
        self.llm: LLM = llm

    async def stream_shell(self, cmd: str) -> AsyncIterator[CodeBaseIOResult]:  # type: ignore
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        while True:
            if process.stdout and (output := await process.stdout.readline()):
                yield CodeBaseIOResult(
                    data=output.decode(),
                    status="healthy",
                )
            if process.stderr and (error := await process.stderr.readline()):
                yield CodeBaseIOResult(
                    data=error.decode(),
                    status="error",
                )
            if process.returncode is not None:
                break

        await process.wait()
        yield CodeBaseIOResult(data="")

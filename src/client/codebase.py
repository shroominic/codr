import asyncio
from typing import AsyncIterator

from funcchain.schema.types import UniversalChatModel as LLM
from websockets import WebSocketClientProtocol

from .shared.codebase.interface import CodebaseInterface
from .shared.schemas import CodebaseIOResult, Data

# todo have a local running script that checks all incoming shell commands for security reasons
# let the user see set his own model optional local model


class CodebaseClient(CodebaseInterface):
    def __init__(self, websocket: WebSocketClientProtocol, llm: LLM) -> None:
        self.websocket = websocket
        self.llm: LLM = llm

    async def stream_shell(self, cmd: str) -> AsyncIterator[CodebaseIOResult]:  # type: ignore
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        while True:
            if process.stdout and (output := await process.stdout.readline()):
                yield CodebaseIOResult(
                    data=output.decode(),
                    status="healthy",
                )
            if process.stderr and (error := await process.stderr.readline()):
                yield CodebaseIOResult(
                    data=error.decode(),
                    status="error",
                )
            if process.returncode is not None:
                break

        await process.wait()
        yield CodebaseIOResult(data="")

    async def read_file(self, path: str) -> CodebaseIOResult:
        with open(path, "r") as file:
            return CodebaseIOResult(data=file.read(), status="healthy")

    async def write_file(self, path: str, data: Data) -> CodebaseIOResult:
        if isinstance(data, bytes):
            data = data.decode()

        with open(path, "w") as file:
            file.write(data)

        return CodebaseIOResult(data="success", status="healthy")

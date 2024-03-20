import asyncio
from typing import AsyncIterator

from funcchain.schema.types import UniversalChatModel as LLM
from shared.codebase.core import Codebase
from shared.schemas import Data  # , CodebaseIOResult
from websockets import WebSocketClientProtocol

# todo have a local running script that checks all incoming shell commands for security reasons
# let the user see set his own model optional local model


class CodebaseClient(Codebase):
    def __init__(self, websocket: WebSocketClientProtocol, llm: LLM) -> None:
        self.websocket = websocket
        self.llm: LLM = llm

    async def shell(self, cmd: str) -> str:
        buffer = ""
        async for output in self.stream_shell(cmd):
            buffer += output
        return buffer

    async def stream_shell(self, cmd: str) -> AsyncIterator[str]:
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        while process.returncode is None:
            if process.stdout and (output := await process.stdout.readline()):
                yield output.decode()

            if process.stderr and (error := await process.stderr.readline()):
                yield error.decode()

    async def read_file(self, path: str) -> str:
        with open(path, "r") as file:
            return file.read()

    async def write_file(self, path: str, data: Data) -> None:
        if isinstance(data, bytes):
            data = data.decode()

        with open(path, "w") as file:
            file.write(data)

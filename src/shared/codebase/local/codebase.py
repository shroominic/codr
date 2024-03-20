import asyncio
from typing import AsyncIterator

from shared.codebase.core import Codebase
from shared.codebase.local.tree import LocalCodebaseTree
from shared.codebase.tree import CodebaseTree
from shared.schemas import Data

# todo add local codebase tree


class LocalCodebase(Codebase):
    def __init__(self, path: str = ".") -> None:
        self.path = path

    @property
    def tree(self) -> type[CodebaseTree]:
        return LocalCodebaseTree  # type: ignore

    async def shell(self, cmd: str) -> str:
        process = await asyncio.create_subprocess_shell(
            cmd,
            cwd=self.path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (stdout + stderr).decode().strip()

    async def stream_shell(self, cmd: str) -> AsyncIterator[str]:  # type: ignore
        process = await asyncio.create_subprocess_shell(
            cmd,
            cwd=self.path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        if process.stdout:
            async for line in process.stdout:
                yield line.decode().strip()

        if process.stderr:
            async for err in process.stderr:
                yield err.decode().strip()

    async def read_file(self, path: str) -> str:
        with open(path, "r") as f:
            return f.read()

    async def write_file(self, path: str, data: Data) -> None:
        with open(path, "w") as f:
            if isinstance(data, bytes):
                data = data.decode()
            f.write(data)

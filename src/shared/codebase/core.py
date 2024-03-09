from abc import ABC, abstractmethod
from typing import AsyncGenerator

from ..codebase.git import CodebaseGit
from ..schemas import Data
from .tree import CodebaseTree


class Codebase(ABC):
    """Interface for the Codebase I/O."""

    # EXTENSIONS

    @property
    def tree(self) -> type[CodebaseTree]:
        return CodebaseTree

    @property
    def git(self) -> CodebaseGit:
        return CodebaseGit(self)

    # EXECUTE

    @abstractmethod
    async def shell(self, cmd: str) -> str: ...

    @abstractmethod
    async def stream_shell(self, cmd: str) -> AsyncGenerator[str, None]: ...

    # FILE CRUD

    async def create_file(self, path: str, data: Data) -> None:
        return await self.write_file(path, data)

    @abstractmethod
    async def read_file(self, path: str) -> str: ...

    @abstractmethod
    async def write_file(self, path: str, data: Data) -> None: ...

    async def delete_file(self, path: str) -> None:
        await self.shell(f"rm {path}")

    # DIRERCTORY CRUD

    async def create_dir(self, path: str) -> None:
        await self.shell(f"mkdir -p {path}")

    async def list_dir(self, path: str) -> list[str]:
        return (await self.shell(f"ls {path}")).split("\n")

    async def rename_dir(self, path: str, new_path: str) -> None:
        await self.shell(f"mv {path} {new_path}")

    async def remove_dir(self, path: str) -> None:
        await self.shell(f"rm -r {path}")

    async def copy(self, path: str, new_path: str) -> None:
        await self.shell(f"cp -r {path} {new_path}")

    async def move(self, path: str, new_path: str) -> None:
        await self.shell(f"mv {path} {new_path}")

    async def fix_file_path(self, path: str) -> str:
        return "todo"

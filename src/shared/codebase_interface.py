from abc import ABC, abstractmethod
from typing import AsyncIterator

from .schemas import CodeBaseIOResult, Data


class CodebaseInterface(ABC):
    """Interface for the codebase I/O."""

    # EXECUTE

    # @abstractmethod
    # async def exec_shell(self, cmd: str) -> CodeBaseIOResult: ...

    @abstractmethod
    async def stream_shell(self, cmd: str) -> AsyncIterator[CodeBaseIOResult]: ...

    # todo have a local running script that checks all incoming shell commands for security reasons
    # let the user see set his own model optional local model

    # FILE CRUD

    # @abstractmethod
    # async def create_file(self, path: str, data: Data) -> CodeBaseIOResult: ...

    @abstractmethod
    async def read_file(self, path: str) -> CodeBaseIOResult: ...

    @abstractmethod
    async def write_file(self, path: str, data: Data) -> CodeBaseIOResult: ...

    # @abstractmethod
    # # can be shell command
    # async def delete_file(self, path: str) -> CodeBaseIOResult: ...

    # # DIRERCTORY CRUD

    # @abstractmethod
    # # can be shell command
    # async def create_dir(self, path: str) -> CodeBaseIOResult: ...

    # @abstractmethod
    # # can be shell command
    # async def list_dir(self, path: str) -> CodeBaseIOResult: ...

    # @abstractmethod
    # # can be shell command
    # async def rename_dir(self, path: str, new_path: str) -> CodeBaseIOResult: ...

    # @abstractmethod
    # # can be shell command
    # async def remove_dir(self, path: str) -> CodeBaseIOResult: ...

    # @abstractmethod
    # # can be shell command
    # async def copy(self, path: str, new_path: str) -> CodeBaseIOResult: ...

    # @abstractmethod
    # # can be shell command
    # async def move(self, path: str, new_path: str) -> CodeBaseIOResult: ...

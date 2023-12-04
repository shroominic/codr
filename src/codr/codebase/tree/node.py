from pathlib import Path
from typing import Union
from abc import ABC, abstractmethod

from pydantic import BaseModel


class CodeBaseNode(BaseModel, ABC):
    name: str
    sha256: str
    embedding: list[float] | None = None

    @property
    def path(self) -> Path:
        return Path(".") / self.name

    @path.setter
    def path(self, value: Union[str, Path]) -> None:
        self.name = Path(value).relative_to(Path.cwd()).as_posix()

    @abstractmethod
    async def refresh(self) -> "CodeBaseNode":
        ...

    def __str__(self, indent: int = 0) -> str:
        return " " * indent + f"Node: {self.path.name}"

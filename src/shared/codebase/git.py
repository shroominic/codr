from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import Codebase


class CodebaseGit:
    def __init__(self, Codebase: "Codebase"):
        self.codebase = Codebase

    async def prepare_environment(self, task: str) -> None:
        pass

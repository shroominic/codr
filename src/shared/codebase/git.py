from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import Codebase


class CodebaseGit:
    def __init__(self, codebase: "Codebase"):
        self.codebase = codebase

    async def prepare_environment(self, task: str) -> None:
        pass

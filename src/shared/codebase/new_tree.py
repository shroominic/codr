from abc import ABC, abstractmethod
from typing import Self

from .core import Codebase


class CodebaseTree(ABC):
    @abstractmethod
    @classmethod
    def load(cls, Codebase: Codebase) -> Self:
        pass

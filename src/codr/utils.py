from typing import Any
from funcchain import settings  # TODO: not use funcchain settings


def log(*text: Any, **kwargs: Any) -> None:
    if settings.DEBUG:
        print(*text, **kwargs)

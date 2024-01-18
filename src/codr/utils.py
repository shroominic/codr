from typing import Any

from rich import print


def log(*text: Any, **kwargs: Any) -> None:
    print(*text, **kwargs)

import asyncio
import sys
import termios
from typing import Callable, Optional


async def set_char_mode(fd: int) -> Optional[list[int]]:
    """
    Asynchronously sets the terminal to read characters one at a time rather than line-by-line.
    """
    old_settings = termios.tcgetattr(fd)
    new_settings = termios.tcgetattr(fd)
    new_settings[3] = new_settings[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
    return old_settings


async def restore_char_mode(fd: int, old_settings: list[int]) -> None:
    """
    Asynchronously restores the terminal to its original settings.
    """
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # type: ignore


async def type_stream(char_callable: Callable[[str], None]) -> None:
    """
    Asynchronously handles each character input by calling a specified function with the character.

    Parameters:
    - char_callable (Callable[[str], None]): A function to call with each character input.
    """
    print("Type something and see it echoed back. Type Ctrl-C to exit.")
    fd = sys.stdin.fileno()
    old_settings = await set_char_mode(fd)

    try:
        while True:
            await asyncio.sleep(0.001)
            char = sys.stdin.read(1)
            if char:
                char_callable(char)
    except KeyboardInterrupt:
        pass
    finally:
        if old_settings:
            await restore_char_mode(fd, old_settings)

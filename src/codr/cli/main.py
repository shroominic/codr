import asyncio
from sys import argv

if __name__ == "__main__":
    from ..commands.chat import dynamic_request
    from .cli import app as typer

    cmds = [c.callback.__name__ for c in typer.registered_commands if c.callback]
    if len(argv) > 1 and argv[1] in cmds:
        # typer handles explicit cli commands
        typer()
    else:
        # dynamic handling of cli request
        instruction = " ".join(argv[1:])
        # asyncio.run(dynamic_request(codr, instruction))

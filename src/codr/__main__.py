from sys import argv

from funcchain import settings

settings.llm = "gpt-4-turbo-preview"


if __name__ == "__main__":
    from .chat import dynamic_request
    from .cli import app as typer

    cmds = [c.callback.__name__ for c in typer.registered_commands if c.callback]
    if len(argv) > 1 and argv[1] in cmds:
        # typer handles explicit cli commands
        typer()
    else:
        # dynamic handling of cli request
        instruction = " ".join(argv[1:])
        dynamic_request(instruction)

import sys
from enum import Enum

from funcchain import chain
from pydantic import BaseModel


class CLICommand(str, Enum):
    EXIT = "exit"
    CHAT = "chat"
    IMPLEMENT = "implement"
    DEBUG = "debug"
    COMMIT = "commit"
    ASK = "ask"


class CLISelector(BaseModel):
    selection: CLICommand


def router(user_request: str) -> CLISelector:
    """
    Select the appropriate cli command/action based on what the user wants.
    """
    return chain()


def chat() -> None:
    cli_input = " ".join(sys.argv[1:])

    route = router(cli_input)

    print(route)

    match route.selection:
        case CLICommand.CHAT:
            print("Chatting")
        case CLICommand.DEBUG:
            print("Debugging")
        case CLICommand.COMMIT:
            print("Commiting")
        case CLICommand.ASK:
            print("Asking")
        case CLICommand.EXIT:
            print("Exiting")
        case CLICommand.IMPLEMENT:
            print("Implementing")
        case _:
            print("Unknown command")


if __name__ == "__main__":
    chat()

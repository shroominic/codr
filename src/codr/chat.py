import sys
from enum import Enum

from funcchain.syntax.components import RouterChat


class CLICommand(str, Enum):
    EXIT = "exit"
    CHAT = "chat"
    IMPLEMENT = "implement"
    DEBUG = "debug"
    COMMIT = "commit"
    ASK = "ask"


router = RouterChat(
    routes={
        "implement": {
            "handler": None,
            "description": "Select this if the user wants you to implement a feature.",
        },
        "debug": {
            "handler": None,
            "description": "Select this if the user wants you to debug the codebase.",
        },
        "commit": {
            "handler": None,
            "description": "Select if the user wants to commit changes.",
        },
        "ask": {
            "handler": None,
            "description": "Select if the user asks a question.",
        },
        "exit": {
            "handler": None,
            "description": "Select if the user wants to exit the chat.",
        },
    }
)


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

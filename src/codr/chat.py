import sys

from funcchain.syntax.components import RouterChat
from funcchain.syntax.components.handler import create_chat_handler
from langchain_core.messages import HumanMessage

router = RouterChat(
    routes={
        "implement": {
            "handler": create_chat_handler(),
            "description": "Select this if the user wants you to implement a feature.",
        },
        "debug": {
            "handler": create_chat_handler(),
            "description": "Select this if the user wants you to debug the codebase.",
        },
        "commit": {
            "handler": create_chat_handler(),
            "description": "Select if the user wants to commit changes.",
        },
        "ask": {
            "handler": create_chat_handler(),
            "description": "Select if the user asks a question.",
        },
        "exit": {
            "handler": create_chat_handler(),
            "description": "Select if the user wants to exit the chat.",
        },
    }
)


def chat() -> None:
    cli_input = " ".join(sys.argv[1:])

    result = router.invoke(input=HumanMessage(content=cli_input))

    print(result)


if __name__ == "__main__":
    chat()

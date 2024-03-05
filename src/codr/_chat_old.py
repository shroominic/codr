import sys

from funcchain.syntax.components import RouterChat
from funcchain.syntax.components.handler import create_chat_handler
from langchain_core.messages import HumanMessage

router = RouterChat(
    routes={
        "implement": {
            "handler": create_chat_handler(),
            "description": "Select this if the user wants you to implement a feature.",
            # "examples": ["todo add"],
        },
        "debug": {
            "handler": create_chat_handler(),
            "description": "Select this if the user wants you to debug the codebase.",
            # "examples": ["todo add"],
        },
        "commit": {
            "handler": create_chat_handler(),
            "description": "Select if the user wants to commit changes.",
            # "examples": ["todo add"],
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


def chat(instruction: str) -> None:
    result = router.invoke(input=HumanMessage(content=instruction))

    print(result.content)


if __name__ == "__main__":
    chat(" ".join(sys.argv[1:]))

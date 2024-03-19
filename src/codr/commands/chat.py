from funcchain import chain
from funcchain.schema.types import UniversalChatModel as LLM
from shared.codebase.core import Codebase
from shared.schemas.actions import (
    Action,
    AskCodebase,
    Commit,
    Debug,
    Help,
    Implement,
    Shell,
    Unexpected,
)

from .. import commands


def handle_dynamic_request(
    instruction: str,
) -> Action:
    """
    The instruction is user input given to a CLI which does not match the required schema.
    Convert it into a valid request so it can be executed correctly.
    """
    return chain()


async def dynamic_request(codebase: Codebase, llm: LLM, instruction: str) -> None:
    match action := handle_dynamic_request(instruction):
        case Implement():
            await commands.exec_implement(codebase, llm, action)

        case Debug():
            await commands.exec_debug(codebase, llm, action)

        case Commit():
            await commands.exec_commit(codebase, llm, action)

        case Shell():
            await commands.exec_shell(codebase, llm, action)

        case AskCodebase():
            await commands.exec_ask(codebase, llm, action)

        case Help():
            print("Help is not implemented yet.\n", action)

        case Unexpected():
            print("Unexpected instruction:\n", action.error_message)

        case _:
            raise ValueError(f"Unhandled action: {action}")

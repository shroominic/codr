from funcchain import chain

from ..core import Codr
from ..shared.schemas.actions import (
    Action,
    AskCodebase,
    Commit,
    Debug,
    Help,
    Implement,
    Shell,
    Unexpected,
)


def handle_dynamic_request(
    instruction: str,
) -> Action:
    """
    The instruction is user input given to a CLI which does not match the required schema.
    Convert it into a valid request so it can be executed correctly.
    """
    return chain()


async def dynamic_request(codr: Codr, instruction: str) -> None:
    match action := handle_dynamic_request(instruction):
        case Implement():
            await codr.implement(action)

        case Debug():
            await codr.debug(action)

        case Commit():
            await codr.commit(action)

        case Shell():
            await codr.shell(action)

        case AskCodebase():
            await codr.ask(action)

        case Help():
            await codr.help(action)

        case Unexpected():
            await codr.unexpected(action)

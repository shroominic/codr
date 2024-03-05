import sys

from funcchain import achain
from pydantic import BaseModel, Field
from rich import print


class Implement(BaseModel):
    """
    Represents a task implementation request. Select this model when you need to specify a task to be solved,
    optionally including a command for debugging purposes.
    """

    task: str = Field(..., description="Description of the task to solve.")
    debug_cmd: str | None = Field(None, description="Command to debug the task.")


class Debug(BaseModel):
    """
    Represents a debugging session request. Use this model when initiating a debug process for your application,
    allowing specification of the startup command, desired output, focus file, and whether to loop the debug process.
    """

    command: str = Field(..., description="Command to startup your app.")
    goal: str | None = Field(None, description="Desired output of the program.")
    focus: str | None = Field(None, description="Focus on a specific file.")
    loop: bool = Field(True, description="Loop the debug process. (default: True)")


class Commit(BaseModel):
    """
    Choose this model when the instruction is about committing changes to the codebase.
    """

    stage: bool = Field(False, description="Stage all changes to commit everything changed. (default: False)")
    push: bool = Field(False, description="Push everything after committing. (default: False)")
    no_group: bool = Field(False, description="Commit every file individually. (default: False)")


class Shell(BaseModel):
    """
    Call this if the instruction is about doing that involves running terminal commands.
    """

    instruction: str = Field(..., description="Instruction to execute.")
    auto_execute: bool = Field(False, description="Automatically execute the command without asking.")


class AskCodebase(BaseModel):
    """
    Represents a request to inquire about the codebase.
    Choose this when the instruction asks a question regarding the codebase
    or coding related information.
    """

    question: str = Field(..., description="Question to ask about the codebase.")


class Help(BaseModel):
    """
    Represents a request for help with the CLI.
    Use this for seeking assistance or information about the CLI.
    """

    question: str = Field(..., description="Question to ask for help about the cli.")
    command: str | None = Field(None, description="Command to get help for.")


class Unexpected(BaseModel):
    """
    Represents an unexpected error message.
    This should be called when the instruction is strange
    or outside the normal flow of operations.
    """

    error_message: str = Field(..., description="Error message to display to the user.")


class CasualChatting(BaseModel):
    """
    Represents a casual chatting request.
    """

    message: str = Field(..., description="Message to chat with the bot.")


async def handle_dynamic_request(
    instruction: str,
) -> Implement | Debug | Commit | Shell | AskCodebase | Help | Unexpected:
    """
    The instruction is user input given to a CLI which does not match the required schema.
    Convert it into a valid request so it can be executed correctly.
    """
    return await achain()


def dynamic_request(instruction: str) -> None:
    import asyncio

    action = asyncio.run(handle_dynamic_request(instruction))

    print(action)

    match action.__class__.__name__:
        case "Implement":
            print("Implement action")
        case "Debug":
            print("Debug action")
        case "Commit":
            print("Commit action")
        case "Shell":
            print("Shell action")
        case "AskCodebase":
            print("AskCodebase action")
        case "Help":
            print("Help action")
        case "Unexpected":
            print("Unexpected action")


if __name__ == "__main__":
    dynamic_request(" ".join(sys.argv[1:]))

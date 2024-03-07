import sys

from funcchain import chain
from pydantic import BaseModel, Field
from rich import print

from .. import cli


class Implement(BaseModel):
    """
    Represents a task implementation request. Select this model when you need to specify a task to be solved,
    optionally including a command for debugging purposes.
    """

    task: str = Field(description="Description of the task to solve.")
    debug_cmd: str | None = Field(None, description="Command to debug the task.")


class Debug(BaseModel):
    """
    Represents a debugging session request. Use this model when initiating a debug process for your application,
    allowing specification of the startup command, desired output, focus file, and whether to loop the debug process.
    """

    command: str = Field(description="Command to startup your app. (set 'undefined' if specific command is not known)")
    goal: str = Field(description="Description of the goal state to check if debugging succeeded.")
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

    instruction: str = Field(description="Instruction in english explaining what to do and the goal.")
    # auto_execute: bool = Field(False, description="False unless the instruction tells specifically.")


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


def handle_dynamic_request(
    instruction: str,
) -> Implement | Debug | Commit | Shell | AskCodebase | Help | Unexpected:
    """
    The instruction is user input given to a CLI which does not match the required schema.
    Convert it into a valid request so it can be executed correctly.
    """
    return chain()


def dynamic_request(instruction: str) -> None:
    action = handle_dynamic_request(instruction)
    print(action)
    match action:
        case Implement(task=task, debug_cmd=debug_cmd):
            cli.implement(task, debug_cmd)

        case Debug(command=command, goal=goal, focus=focus, loop=loop):
            cli.debug(command, goal, focus, loop)

        case Commit(stage=stage, push=push, no_group=no_group):
            cli.commit(stage, push, no_group)

        case Shell(instruction=instr):
            cli.shell(instr)

        case AskCodebase(question=question):
            cli.ask(question)

        case Help(question=question, command=command):
            print("no help sry")

        case Unexpected(error_message=error_message):
            print("ERROR:", error_message)


if __name__ == "__main__":
    dynamic_request(" ".join(sys.argv[1:]))

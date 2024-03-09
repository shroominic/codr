from pydantic import BaseModel, Field


class Implement(BaseModel):
    """
    Represents a task implementation request. Select this model when you need to specify a task to be solved,
    optionally including a command for debugging purposes.
    """

    task: str = Field(description="Description of the task to solve.")
    debug_cmd: str | None = Field(description="Optional command to debug the task. ('None' if not given)")


class Debug(BaseModel):
    """
    Represents a debugging session request. Use this model when initiating a debug process for your application,
    allowing specification of the startup command, desired output, focus file, and whether to loop the debug process.
    """

    command: str = Field(description="Command to startup your app. (set 'undefined' if specific command is not known)")
    goal: str = Field(
        default="healthy console output", description="Description of the goal state to check if debugging succeeded."
    )
    focus: str | None = Field(default=None, description="Focus on a specific file.")
    loop: bool = Field(default=True, description="Loop the debug process. (default: True)")


class Commit(BaseModel):
    """
    Choose this model when the instruction is about committing changes to the Codebase.
    """

    stage: bool = Field(default=False, description="Stage all changes to commit everything changed. (default: False)")
    push: bool = Field(default=False, description="Push everything after committing. (default: False)")
    no_group: bool = Field(default=False, description="Commit every file individually. (default: False)")


class Shell(BaseModel):
    """
    Call this if the instruction is about doing that involves running terminal commands.
    """

    instruction: str = Field(description="Instruction in english explaining what to do and the goal.")
    auto_execute: bool = Field(
        default=False, description="False unless the instruction tells explicitly to auto execute."
    )


class AskCodebase(BaseModel):
    """
    Represents a request to inquire about the Codebase.
    Choose this when the instruction asks a question regarding the Codebase
    or coding related information.
    """

    question: str = Field(description="Question to ask about the Codebase.")


class Help(BaseModel):
    """
    Represents a request for help with the CLI.
    Use this for seeking assistance or information about the CLI.
    """

    question: str = Field(description="Question to ask for help about the cli.")
    command: str | None = Field(None, description="Command to get help for.")


class Unexpected(BaseModel):
    """
    Represents an unexpected error message.
    This should be called when the instruction is strange
    or outside the normal flow of operations.
    """

    error_message: str = Field(description="Error message to display to the user.")


class CasualChatting(BaseModel):
    """
    Represents a casual chatting request.
    """

    message: str = Field(description="Message to chat with the bot.")


Action = Implement | Debug | Commit | Shell | AskCodebase | Help | Unexpected | CasualChatting

import asyncio
from typing import Annotated, Optional

import typer
from codr.core import Codr
from funcchain import settings

from .codebase_local import LocalCodebase

settings.llm = "gpt-4-turbo-preview"

app = typer.Typer()

codr = Codr(
    Codebase=LocalCodebase(),
    llm="gpt-4-turbo-preview",
)


@app.command()
def implement(
    task: Annotated[
        str,
        typer.Argument(help="Description of the task to solve."),
    ],
    debug_cmd: Annotated[
        Optional[str],
        typer.Option(help="Command to debug the task."),
    ] = None,
) -> None:
    """
    Input a task description and the llm agent will try to solve it.
    """
    asyncio.run(codr.implement(task=task, debug_cmd=debug_cmd))


@app.command()
def debug(
    command: Annotated[
        str,
        typer.Argument(help="Command to startup your app."),
    ],
    goal: Annotated[
        str,
        typer.Option(help="Desired output of the program."),
    ] = "healthy console ouput",
    focus: Annotated[
        Optional[str],
        typer.Option(help="Focus on a specific file."),
    ] = None,
    loop: Annotated[
        bool,
        typer.Option(help="Loop the debug process."),
    ] = True,
) -> None:
    """
    Automatically debug with the llm agent.
    """
    asyncio.run(codr.debug(command, goal, focus, loop))


@app.command()
def commit(
    stage: Annotated[
        bool,
        typer.Option("--stage", "-s", help="Stage all changes to commit everything changed."),
    ] = False,
    push: Annotated[
        bool,
        typer.Option("--push", "-p", help="Push everything after commiting."),
    ] = False,
    no_group: Annotated[
        bool,
        typer.Option("--no-group", "-n", help="Commit every file individually."),
    ] = False,
) -> None:
    """
    Write commit messages and commit changes.
    """
    asyncio.run(codr.commit(stage, push, no_group))


@app.command()
def shell(
    instruction: Annotated[str, typer.Argument(help="Instruction to execute.")],
    auto_execute: Annotated[
        bool,
        typer.Option("--auto", "-a", help="Automatically execute the command without asking."),
    ] = False,
) -> None:
    """
    Write a shell command to fulfill the instruction.
    """
    asyncio.run(codr.shell(instruction, auto_execute))


@app.command()
def ask(
    question: Annotated[str, typer.Argument(help="Question to ask.")],
) -> None:
    """
    Ask a question about the Codebase or relevant libraries.
    """
    asyncio.run(codr.ask(question))


@app.command()
def chat() -> None:
    """
    Open CLI Chat Interface
    """
    # from .llm.chat import chat

    # asyncio.run(chat())


def auto_linter() -> None:
    """
    Automatically run a linter on the Codebase and fix issues.
    Also include mypy and flake8.
    """

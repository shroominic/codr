import asyncio
from typing import Annotated, Optional

import typer
from rich import print

from .commands import auto_debug, commit_changes, execute_shell, expert_answer, solve_task

app = typer.Typer()


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
    asyncio.run(solve_task(task, debug_cmd))


@app.command()
def debug(
    command: Annotated[
        str,
        typer.Argument(help="Command to startup your app."),
    ],
    goal: Annotated[
        Optional[str],
        typer.Option(help="Desired output of the program."),
    ] = None,
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
    if focus:
        print("Focus on: ", focus, " (not implemented yet)")
    asyncio.run(auto_debug(command, goal or "healthy console output", loop))


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
    asyncio.run(commit_changes(stage, push, no_group))


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
    asyncio.run(execute_shell(instruction, auto_execute))


@app.command()
def ask(
    question: Annotated[str, typer.Argument(help="Question to ask.")],
) -> None:
    """
    Ask a question about the codebase or relevant libraries.
    """
    asyncio.run(expert_answer(question))


@app.command()
def chat() -> None:
    """
    Open CLI Chat Interface
    """
    # from .llm.chat import chat

    # asyncio.run(chat())


def auto_linter() -> None:
    """
    Automatically run a linter on the codebase and fix issues.
    Also include mypy and flake8.
    """

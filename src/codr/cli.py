import asyncio
from typing import Annotated, Optional

import typer
from rich import print

from .commands import commit_changes, auto_debug, expert_answer, solve_task

app = typer.Typer()


@app.command()
def implement(
    task: Annotated[str, typer.Argument(help="Description of the task to solve.")],
    debug_cmd: Annotated[
        Optional[str], typer.Option(help="Command to debug the task.")
    ] = None,
) -> None:
    """
    Input a task description and the llm agent will try to solve it.
    """
    asyncio.run(solve_task(task, debug_cmd))


@app.command()
def debug(
    command: Annotated[str, typer.Argument(help="Command to startup your app.")],
    goal: Annotated[
        Optional[str], typer.Option(help="Desired output of the program.")
    ] = None,
    focus: Annotated[
        Optional[str], typer.Option(help="Focus on a specific file.")
    ] = None,
    loop: Annotated[bool, typer.Option(help="Loop the debug process.")] = True,
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
        typer.Option(
            "--stage", "-s", help="Stage all changes to commit everything changed."
        ),
    ] = False,
    push: Annotated[
        bool, typer.Option("--push", "-p", help="Push everything after commiting.")
    ] = False,
) -> None:
    """
    Write commit messages and commit changes.
    """
    asyncio.run(commit_changes(stage, push))


@app.command()
def ask(
    question: Annotated[str, typer.Argument(help="Question to ask.")],
) -> None:
    """
    Ask a question about the codebase or relevant libraries.
    """
    print(asyncio.run(expert_answer(question)))


@app.command()
def tree() -> None:
    """
    Print the current tree.
    """
    from .codebase.tree import CodeBaseTree

    tree = asyncio.run(CodeBaseTree.load())
    print(tree.__str__())


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

import asyncio
from typing import Annotated, Optional

import typer
from funcchain import settings
from rich import print

from .llm.scripts import auto_debug, commit_changes, expert_answer, solve_task
from .llm.templates import solve_task_system_instruction

app = typer.Typer()

settings.DEFAULT_SYSTEM_PROMPT = solve_task_system_instruction
settings.MODEL_NAME = "gpt-4-1106-preview"


@app.command()
def solve(
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
    asyncio.run(auto_debug(command, goal, loop))


# better debug
# select relevant files based on console output
# give all relevant files in context
# choose files to edit
# edit files and iterate over debug process


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


if __name__ == "__main__":
    app()

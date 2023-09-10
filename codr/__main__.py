import asyncio

import typer
from typing import Annotated, Optional

from codr.llm.scripts import solve_task, auto_debug, commit_changes
from codr.llm.templates import solve_task_system_instruction
from funcchain import settings
from rich import print

app = typer.Typer()

settings.DEFAULT_SYSTEM_PROMPT = solve_task_system_instruction


@app.command()
def solve(
    task: Annotated[str, typer.Argument(help="Description of the task to solve.")],
    debug_cmd: Annotated[Optional[str], typer.Option(help="Command to debug the task.")] = None,
) -> None:
    """
    Input a task description and the llm agent will try to solve it.
    """
    asyncio.run(solve_task(task, debug_cmd))


@app.command()
def debug(
    command: Annotated[str, typer.Argument(help="Command to startup your app.")],
    goal: Annotated[Optional[str], typer.Option(help="Desired output of the program.")] = None,
    focus: Annotated[Optional[str], typer.Option(help="Focus on a specific file.")] = None,
    loop: Annotated[bool, typer.Option(help="Loop the debug process.")] = True,
) -> None:
    """
    Automatically debug with the llm agent.
    """
    if focus: print("Focus on: ", focus, " (not implemented yet)")
    asyncio.run(auto_debug(command, goal, loop))


@app.command()
def commit():
    """
    Write commit messages and commit changes.
    """
    asyncio.run(commit_changes())


@app.command()
def ask(
    question: Annotated[str, typer.Argument(help="Question to ask.")],
) -> None:
    """
    Ask a question about the codebase or relevant libraries.
    """
    print("Answering: ", question)
    print("Not implemented yet.")
    # TODO: use ask to improve task solving


@app.command()
def tree():
    """
    Print the current tree.
    """
    from codr.codebase.tree import CodeBaseTree

    tree = asyncio.run(CodeBaseTree.load())
    print(tree.nodes)


@app.command()
def test():
    print("Test successful!")


if __name__ == "__main__":
    app()

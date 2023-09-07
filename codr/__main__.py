import asyncio

import typer

from codr.llm.scripts import solve_task, auto_debug, commit_changes
from codr.llm.templates import solve_task_system_instruction
from funcchain import settings

app = typer.Typer()

settings.DEFAULT_SYSTEM_PROMPT = solve_task_system_instruction


@app.command()
def solve(task_description: str):
    """
    Input a task description and the llm agent will try to solve it.
    """
    asyncio.run(solve_task(task_description))


@app.command()
def debug(command: str):
    """
    Automatically debug with the llm agent.
    """
    asyncio.run(auto_debug(command))


@app.command()
def commit():
    """
    Write commit messages and commit changes.
    """
    asyncio.run(commit_changes())


@app.command()
def tree():
    """
    Print the current tree.
    """
    from codr.codebase.tree import CodeBaseTree
    typer.echo(
        asyncio.run(CodeBaseTree.load())
    )


@app.command()
def test():
    typer.echo("Test successful!")


if __name__ == "__main__":
    app()

import asyncio
from typing import Annotated, Optional

import typer
from funcchain import settings
from funcchain.utils.model_defaults import create_long_llm
from rich import print

from codr.llm.scripts import auto_debug, commit_changes, solve_task, expert_answer
from codr.llm.templates import solve_task_system_instruction

app = typer.Typer()

settings.DEFAULT_SYSTEM_PROMPT = solve_task_system_instruction
settings.LLM = create_long_llm()


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
    if focus:
        print("Focus on: ", focus, " (not implemented yet)")
    asyncio.run(auto_debug(command, goal, loop))


@app.command()
def commit() -> None:
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
    print(asyncio.run(expert_answer(question)))


@app.command()
def tree() -> None:
    """
    Print the current tree.
    """
    from codr.codebase.tree import CodeBaseTree

    tree = asyncio.run(CodeBaseTree.load())
    print(tree.__str__())


@app.command()
def chat() -> None:
    """
    Open CLI Chat Interface
    """
    # from codr.llm.chat import chat

    # asyncio.run(chat())


if __name__ == "__main__":
    app()

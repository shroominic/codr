import asyncio
import sys
from typing import Annotated, Optional

import typer
from codr import Codr
from shared.codebase.local.codebase import LocalCodebase

cli = typer.Typer()

codr = Codr(codebase=LocalCodebase(), llm="gpt-4o")


@cli.command()
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


@cli.command()
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


@cli.command()
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


@cli.command()
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


@cli.command()
def ask(
    question: Annotated[str, typer.Argument(help="Question to ask.")],
) -> None:
    """
    Ask a question about the Codebase or relevant libraries.
    """
    asyncio.run(codr.ask(question))


@cli.command()
def chat(instruction: Annotated[str, typer.Argument(help="Instruction to execute.")] = "") -> None:
    """
    Open CLI Chat Interface
    """
    asyncio.run(codr.chat(instruction))


def auto_linter() -> None:
    """
    Automatically run a linter on the Codebase and fix issues.
    Also include mypy and flake8.
    """


def main() -> None:
    args = [arg for arg in sys.argv[1:]]
    cmds = [c.callback.__name__ for c in cli.registered_commands if c.callback]
    cmds.extend(["--help", "--install-completion", "--show-completion"])

    # > codr
    if len(args) == 0:
        return asyncio.run(codr.chat())

    # > codr <command>
    if len(args) > 0 and args[0] in cmds:
        return cli()

    # > codr <instruction>
    return asyncio.run(codr.chat(" ".join(args)))


if __name__ == "__main__":
    main()

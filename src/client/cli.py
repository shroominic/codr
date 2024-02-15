from typing import Annotated, Optional

import typer

app = typer.Typer()


@app.command()
def implement(
    task: Annotated[
        str,
        typer.Argument(help="Description of the task to implement."),
    ],
    debug_cmd: Annotated[
        Optional[str],
        typer.Option(help="Command to debug the task."),
    ] = None,
) -> None:
    """
    Input a task description and the llm agent will try to implement it.
    """
    ...


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
    ...


@app.command()
def commit(
    stage: Annotated[
        bool,
        typer.Option(
            "--stage",
            "-s",
            help="Stage all changes to commit everything changed.",
        ),
    ] = False,
    push: Annotated[
        bool,
        typer.Option("--push", "-p", help="Push everything after commiting."),
    ] = False,
) -> None:
    """
    Write commit messages and commit changes.
    """
    ...


@app.command()
def ask(
    question: Annotated[
        str,
        typer.Argument(help="Question to ask."),
    ],
) -> None:
    """
    Ask a question about the codebase or relevant libraries.
    """
    ...


@app.command()
def tree() -> None:
    """
    Print the current tree.
    """
    ...


@app.command()
def chat() -> None:
    """
    Open CLI Chat Interface
    """
    ...

import platform
from typing import Annotated, Any

from funcchain import achain
from funcchain.syntax.params import Depends
from InquirerPy import inquirer
from rich import print


def gather_system_info(*_: Any) -> str:
    return (
        f"OS: {platform.system()}\n"
        f"Version: {platform.version()}\n"
        f"Machine: {platform.machine()}\n"
        f"Processor: {p if (p := platform.processor()) else 'Unknown'}\n"
    )


async def write_shell_command(
    instruction: str,
    system_info: Annotated[str, Depends(gather_system_info)] = "",
) -> list[str]:
    """
    Write one or a series of shell commands to fulfill the instruction.
    Output a list of strings with the commands to execute.
    If its only one command, output a list with a single string.
    """
    return await achain()


async def execute_shell(instruction: str, auto_execute: bool = False) -> None:
    ask_exec = inquirer.select("Execute the following command?", choices=["Yes", "No"])
    for command in await write_shell_command(instruction):
        print(f"> [green]{command}[/green]")
        if auto_execute or await ask_exec.execute_async():  # type: ignore
            print("executing cmd")

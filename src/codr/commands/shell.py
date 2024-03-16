import platform
from typing import Annotated, Any, Literal

from funcchain import achain
from funcchain.schema.types import UniversalChatModel as LLM
from funcchain.syntax.params import Depends
from InquirerPy import inquirer
from pydantic import BaseModel, Field
from rich import print
from shared.codebase.core import Codebase
from shared.schemas import Shell


def gather_system_info(*_: Any) -> str:
    return (
        f"OS: {platform.system()}\n"
        f"Version: {platform.version()}\n"
        f"Machine: {platform.machine()}\n"
        f"Processor: {p if (p := platform.processor()) else 'Unknown'}\n"
    )


async def exec_shell(codebase: Codebase, llm: LLM, input: Shell) -> None:
    """commit command wrapper"""

    async def write_shell_command(
        instruction: str,
        system_info: Annotated[str, Depends(gather_system_info)] = "",
    ) -> list[str]:
        """
        Write one or a series of shell commands to fulfill the instruction.
        Output a list of strings with the commands to execute.
        If its only one command, output a list with a single string.
        """
        return await achain(settings_override={"llm": llm})

    async def analyze_output(
        command: str,
        console_output: str,
    ) -> Literal["healthy", "unhealthy", "unknown"]:
        """
        Analyze the console output to determine if the goal state was reached.
        Return either "healthy", "unhealthy", or "unknown" if the output is not clear.
        """
        return await achain(settings_override={"llm": llm})

    class FixedCommand(BaseModel):
        thought: str = Field(description="Description of what went wrong and how to fix it.")
        command: str = Field(description="Fixed shell command to execute.")

    async def fix_command(command: str, output: str) -> FixedCommand:
        """
        The command failed (see provided output) and needs to be adjusted.
        Write a new shell command and a description of what went wrong, how to fix it.
        """
        return await achain(settings_override={"llm": llm})

    async def handle_execution(command: str) -> None:
        output = ""
        async for chunk in codebase.stream_shell(command):
            output += chunk
            print(f"[red]{chunk}[/red]")

        if await analyze_output(command, output) == "healthy":
            print("[green]Command executed successfully[/green]")

        elif await analyze_output(command, output) == "unknown":
            print("[yellow]Command executed, but the output is unclear[/yellow]")

        else:
            new_cmd = await fix_command(command, output)
            print(new_cmd)
            print(f"[yellow]Command failed, trying to fix it with: {new_cmd.command}[/yellow]")
            await handle_execution(new_cmd.command)

    async def shell(instruction: str) -> None:
        # todo replace with client interface to ask for confirmation
        ask_exec = inquirer.select("Execute command?", choices=["yes", "no"])
        # add auto execute option loading from config
        for command in await write_shell_command(instruction):
            print(f"> [green]{command}[/green]")
            if (await ask_exec.execute_async()) == "yes":  # type: ignore
                await handle_execution(command)
            else:
                print("[yellow]Command not executed[/yellow]")

    await shell(input.instruction)

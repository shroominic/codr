from funcchain import achain
from ..utils import log

from ..codebase.func import bash


# better debug
# select relevant files based on console output
# give all relevant files in context
# choose files to edit
# edit files and iterate over debug process


async def generate_task(
    console_output: str,
    desired_output: str,
) -> str:
    """
    Generate a task description to fix the error.
    """
    return await achain()


async def check_result(console_output: str) -> bool:
    """
    Is the output healthy? Answer with "yes" or "no".
    """
    return await achain()


async def check_desired_output(
    console_output: str,
    desired_output_description: str,
) -> bool:
    """
    Is the output what is desired? Answer with "yes" or "no".
    """
    return await achain()


async def auto_debug(
    command: str,
    goal: str | None = None,
    loop: bool = False,
) -> None:
    result = await bash(command)

    log("RESULT: ", result)

    if (
        goal
        and await check_desired_output(result, goal)
        or not goal
        and await check_result(result)
    ):
        return log("DEBUG SUCCESSFUL")

    description = await generate_task(result, goal or "healthy")
    log("TASK:", description)

    from .implement import solve_task

    await solve_task(description)

    if loop:
        await auto_debug(command, goal, loop)

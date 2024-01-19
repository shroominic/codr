import asyncio
from datetime import datetime, timedelta
from typing import Any

from funcchain import achain
from pydantic import BaseModel, Field
from rich import print

from ..codebase.func import stream_bash

# better debug
# select relevant files based on console output
# give all relevant files in context
# choose files to edit
# edit files and iterate over debug process

# map funcchain that checks file for debug analysis over all files in codebase


class ConsoleOutputAnalysis(BaseModel):
    """Analyzis of the console output to determine if the result is healthy or not."""

    observation: str = Field(description="Short of what can be observed in the console output.")
    health: bool = Field(description="Is the console output healthy?")
    accuracy: int = Field(description="1-10 accuracy of the health check.")

    def __bool__(self) -> bool:
        return self.health


async def check_result(
    console_output: str,
) -> ConsoleOutputAnalysis:
    """
    Analyze the console output and determine if the result is healthy or not.
    """
    return await achain()


async def check_desired_output(
    console_output: str,
    desired_output_description: str,
) -> ConsoleOutputAnalysis:
    """
    Analyze the console output and determine if the result is healthy or not.
    The user gave a description of the desired output to give you an idea of what healthy means.
    """
    return await achain()


class DetermineLoading(BaseModel):
    """Analyzis of the console output to determine if the result is still loading."""

    observation: str = Field(description="Short description of what can be observed in the console output.")
    loading: bool = Field(description="Is the console output still loading?")
    accuracy: int = Field(description="1-10 accuracy of the loading check.")

    def __bool__(self) -> bool:
        return self.loading


async def check_loading(
    console_output: str,
) -> DetermineLoading:
    """
    Analyze the console output and determine if the result is still loading.
    The input is a snippet of a console stream.
    As examples if packages are still being installed or if something is still being compiled
    -> it is still loading.
    But if the console output is listening for something like a uvicorn worker
    -> it is not loading.
    """
    return await achain()


class DebugTask(BaseModel):
    """Task to fix the codebase to produce a healthy console output."""

    observation: str = Field(description="Short of what can be observed in the console output.")
    goal: str = Field(description="Short of what the console output should be.")
    problem_files: list[str] = Field(description="Files mentioned in the console output that are not healthy.")
    task_description: str = Field(description="Detailed, precise plan on how to fix the problem.")


async def generate_task(
    console_output: str,
    goal: str,
) -> DebugTask:
    """
    Generate a task to fix the codebase to produce a healthy console output.
    """
    return await achain()


async def auto_debug(
    command: str,
    goal: str,
    loop: bool = False,
) -> None:
    result = await analyze_output(command, goal)

    if goal and await check_desired_output(result, goal) or not goal and await check_result(result):
        return print("DEBUG SUCCESSFUL")

    debug_task = await generate_task(result, goal)
    description = debug_task.task_description
    print("DEBUG TASK:", debug_task)

    from .implement import solve_task

    await solve_task(description)

    if loop:
        print("DEBUGGING LOOP:", command)
        await auto_debug(command, goal, loop)


async def analyze_output(command: str, goal: str) -> str:
    """
    Analyze stream of console output and determine if the result is healthy or not.
    """
    interval: int = 5
    live_data: dict[str, Any] = {
        "last_batch_time": datetime.now(),
        "stack": "",
    }

    async def stream_output(
        command: str,
        data: dict[str, Any],
    ) -> None:
        print("👀 watching console output")
        async for batch in stream_bash(command):
            print("\033[91m", batch, "\033[0m")
            data["last_batch_time"] = datetime.now()
            data["stack"] += batch

    asyncio.create_task(stream_output(command, live_data))

    while True:
        await asyncio.sleep(interval)
        if datetime.now() - live_data["last_batch_time"] > timedelta(seconds=5):
            if not await check_loading(live_data["stack"]):
                return live_data["stack"]

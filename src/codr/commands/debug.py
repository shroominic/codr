import asyncio
from datetime import datetime, timedelta
from typing import Annotated, Any

from funcchain import achain, chain, runnable
from funcchain.schema.types import UniversalChatModel as LLM
from funcchain.syntax.params import Depends
from pydantic import BaseModel, Field
from shared.codebase.core import Codebase
from shared.codebase.tree import CodebaseTree
from shared.schemas import Debug, Implement

# better debug
# select relevant files based on console output
# give all relevant files in context
# choose files to edit
# edit files and iterate over debug process

# map funcchain that checks file for debug analysis over all files in Codebase


async def exec_debug(codebase: Codebase, llm: LLM, input: Debug) -> None:
    """commit command wrapper"""

    class ConsoleOutputAnalysis(BaseModel):
        """Analyzis of the console output to determine if the result is healthy or not."""

        observation: str = Field(description="Short of what can be observed in the console output.")
        health: bool = Field(description="Is the console output healthy?")
        accuracy: int = Field(description="1-10 accuracy of the health check.")

        def __bool__(self) -> bool:
            return self.health

    async def check_desired_output(
        console_output: str,
        desired_output_description: str,
    ) -> ConsoleOutputAnalysis:
        """
        Analyze the console output and determine if the result is healthy or not.
        {% if desired_output_description != "healthy console output" %}
        The user gave a description of the desired output to give you an idea of what healthy means:
        {{ desired_output_description }}
        {% endif %}
        """
        return await achain(llm=llm)

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
        return await achain(llm=llm)

    class DebugTask(BaseModel):
        """Task to fix the Codebase to produce a healthy console output."""

        observation: str = Field(description="Short of what can be observed in the console output.")
        goal: str = Field(description="Short of what the console output should be.")
        problem_files: list[str] = Field(description="Files mentioned in the console output that are not healthy.")
        task_description: str = Field(description="Detailed, precise plan on how to fix the problem.")

    @runnable(llm=llm)
    def generate_task(
        goal: str,
        console_output: str,
        codebase_tree: Annotated[CodebaseTree, Depends(codebase.tree.load)],
    ) -> DebugTask:
        """
        Generate a task to fix the Codebase to produce a healthy console output.
        """
        return chain()

    async def auto_debug(
        command: str,
        goal: str,
        loop: bool = False,
    ) -> None:
        result = await analyze_output(command, goal)

        if await check_desired_output(result, goal):
            return print("DEBUG SUCCESSFUL")

        debug_task = await generate_task.ainvoke({"console_output": result, "goal": goal})
        description = debug_task.task_description
        print("DEBUG TASK:", debug_task)

        from .implement import exec_implement

        await exec_implement(codebase, llm, Implement(task=description, debug_cmd=command))

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
            async for batch in codebase.stream_shell(command):  # type: ignore
                print("\033[91m", batch, "\033[0m")
                data["last_batch_time"] = datetime.now()
                data["stack"] += batch

        asyncio.create_task(stream_output(command, live_data))

        while True:
            await asyncio.sleep(interval)
            if datetime.now() - live_data["last_batch_time"] > timedelta(seconds=5):
                # todo add cropping of console log stack
                if not await check_loading(live_data["stack"]):
                    return live_data["stack"]

    await auto_debug(input.command, input.goal, input.loop)

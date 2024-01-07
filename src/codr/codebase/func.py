import asyncio
import os
from datetime import datetime
from os import getenv
from pathlib import Path
from typing import AsyncGenerator

import aiofiles  # type: ignore

from ..schema import Task
from .tree import CodeBaseTree


async def _bash_gen(*commands: str) -> AsyncGenerator[bytes, None]:
    """
    Run a bash command
    """
    process = await asyncio.create_subprocess_shell(
        "\n".join(commands),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()

    if stdout:
        yield stdout
    if stderr:
        yield stderr


async def stream_bash(command: str) -> AsyncGenerator[str, None]:
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    if process.stdout:
        async for line in process.stdout:
            yield line.decode().strip()

    if process.stderr:
        async for err in process.stderr:
            yield err.decode().strip()


async def bash(*commands: str) -> str:
    """
    Run a bash command
    """
    stdout = ""
    async for output in _bash_gen(*commands):
        stdout += output.decode()
    return stdout


def bash_sync(*commands: str) -> str:
    """
    Run a bash command
    """
    return asyncio.run(bash(*commands))


async def read_file(relative_path: str) -> str:
    """
    Read a file from the codebase
    """
    async with aiofiles.open(relative_path) as f:
        return await f.read()


def read_file_sync(relative_path: str) -> str:
    """
    Read a file from the codebase
    """
    with open(relative_path) as f:
        if relative_path.endswith(".py"):
            return "```python\n" + f.read() + "\n```"
        else:
            return "```\n" + f.read() + "\n```"


async def show_tree() -> str:
    """
    Show the codebase tree
    """
    return (await CodeBaseTree.load()).show()


async def get_tree() -> CodeBaseTree:
    """
    Get the codebase tree
    """
    return await CodeBaseTree.load()


async def file_exists(relative_path: str) -> bool:
    """
    Check if a file exists
    """
    return Path(relative_path).exists()


async def create_file(relative_path: str, content: str) -> None:
    """
    Create a file in the codebase. If the directory does not exist, create it.
    """
    dir_name = os.path.dirname(relative_path)
    if dir_name != "" and not os.path.exists(dir_name):
        os.makedirs(dir_name)

    async with aiofiles.open(relative_path, "w") as f:
        await f.write(content)

    # Markdown Formatting
    if relative_path.endswith(".md"):
        if not await bash("which prettier") == "":
            await bash(f"prettier --write {relative_path}")
            return
        print(
            "Prettier is not installed. Please install it with `npm install -g prettier`"
        )

    # Python Formatting
    if relative_path.endswith(".py"):
        await bash(f"black {relative_path}")


async def create_directory(relative_path: str) -> None:
    """
    Create a directory in the codebase
    """
    await bash(f"mkdir {relative_path}")


async def modify_file(relative_path: str, content: str) -> None:
    """
    Replace a file in the codebase
    """
    import aiofiles  # type: ignore

    async with aiofiles.open(relative_path, "w") as f:
        await f.write(content)
    await bash(f"black {relative_path}")


async def delete_file(relative_path: str) -> str:
    """
    Delete a file in the codebase
    """
    return await bash(f"rm {relative_path}")


async def prepare_environment(task: Task) -> None:
    """
    Prepare the git env for the codebase
    """
    if not os.path.exists(".git"):
        await bash("git init")

    # if there are open changes stash them
    if getenv("AUTO_COMMIT", "false").lower() == "true":
        from ..commands import commit_changes

        await commit_changes(True, False)  # TODO: make this configurable

    if getenv("AUTO_STASH", "false").lower() == "true":
        git_status = await bash("git status")
        if "Changes not staged for commit" in git_status:
            stash_result = await bash("git stash")
            if "No local changes to save" in stash_result:
                print("No changes to stash")
            elif "Saved working directory and index state" not in stash_result:
                raise Exception(f"Failed to stash changes: {stash_result}")

    # checkout to new created branch with task name
    if getenv("CHECKOUT_BRANCH", "false").lower() == "true":
        if not task.name:
            task.name = "codr_task"
        task_name = (
            task.name.replace(" ", "_") + "_" + datetime.now().strftime("%Y%m%d%H%M%S")
        )
        checkout_result = await bash(f"git checkout -b {task_name}")
        if "Switched to a new branch" not in checkout_result:
            raise Exception(f"Failed to checkout to new branch: {checkout_result}")

        # apply stash to new branch
        await bash("git stash apply")


async def fix_file_path(
    relative_path: str, codebase_tree: CodeBaseTree | None = None
) -> str:
    """Fix file name to absolute path"""
    tree = codebase_tree or await get_tree()
    file_name = relative_path.split("/")[-1]
    files = [file for file in tree.files if file.name.split("/")[-1] == file_name]

    if len(files) > 1:
        raise Exception(f"Duplicate file name: {file_name}, {files}")
    elif len(files) < 1:
        raise FileNotFoundError(f"File not found: {file_name}, {files}")

    return files[0].name

import os
import asyncio
import aiofiles  # type: ignore
from os import getenv
from datetime import datetime
from typing import AsyncGenerator
from pathlib import Path
from codr.codebase.tree import CodeBaseTree
from codr.llm.schema import Task
    

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
        return f.read()


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


async def create_file(relative_path: str, content: str):
    """
    Create a file in the codebase
    """
    async with aiofiles.open(relative_path, "w") as f:
        await f.write(content)
    await bash(f"black {relative_path}")


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
    git_status = await bash("git status")
    if "Changes not staged for commit" in git_status:
        stash_result = await bash("git stash")
        if "No local changes to save" in stash_result:
            print("No changes to stash")
        elif "Saved working directory and index state" not in stash_result:
            raise Exception(f"Failed to stash changes: {stash_result}")

    # checkout to new created branch with task name
    if getenv("CHECKOUT_TO_NEW_BRANCH", "True") == "True":
        task_name = task.name.replace(" ", "_") + "_" + datetime.now().strftime("%Y%m%d%H%M%S")
        checkout_result = await bash(f"git checkout -b {task_name}")
        if "Switched to a new branch" not in checkout_result:
            raise Exception(f"Failed to checkout to new branch: {checkout_result}")

    # apply stash to new branch
    apply_result = await bash("git stash apply")


async def fix_file_path(relative_path: str) -> str:
    """Fix file name to absolute path"""
    tree = await get_tree()
    file_name = relative_path.split("/")[-1]
    files = [
        file for file in tree.files 
        if file.name.split("/")[-1] == file_name
    ]
    
    if len(files) > 1:
        raise Exception(f"Duplicate file name: {file_name}, {files}")
    elif len(files) < 1:
        raise Exception(f"File not found: {file_name}, {files}")
    
    return files[0].name

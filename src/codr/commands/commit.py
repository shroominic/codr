import asyncio

from funcchain import achain
from rich import print

from ..codebase.func import bash


async def write_commit_message(
    file_name: str,
    modifications: str,
) -> str:
    """
    Write a tiny commit message for these file changes.
    Start with a emoji and never answer with more than 5 words.
    Example: 🐛 Fix bug in foo.py
    """
    return await achain()


async def commit_changes(stage: bool, auto_push: bool) -> None:
    print("Committing changes")
    if stage:
        await bash("git add .")

    git_status = (await bash("git status")).split("Changes not staged for commit:")[0]
    print("bash completed")
    if "Changes to be committed" in git_status:
        commits = [
            asyncio.create_task(process_change(change)) for change in git_status.split("\n") if change.startswith("\t")
        ]
        for task in asyncio.as_completed(commits):
            change, msg = await task
            print(f"[grey]{change}[/grey] > {msg}")
            await bash(f'git commit {change} -m "{msg}"')

        if auto_push:
            await bash("git push")


async def process_change(change: str) -> tuple[str, str]:
    print(change)
    if len(change_split := change.split()) > 1:
        if change_split[0] == "modified:":
            file_change = change_split[1].strip()
            modifications = await bash(f"git diff --staged {file_change}")
            commit_msg = await write_commit_message(file_change, modifications)
            return file_change, commit_msg

        if change_split[0] == "new":
            file_change = change_split[2].strip()
            modifications = await bash(f"git diff --staged {file_change}")
            commit_msg = await write_commit_message(file_change, modifications)
            return file_change, commit_msg

        if change_split[0] == "deleted:":
            file_change = change_split[1].strip()
            commit_msg = await write_commit_message(file_change, "got deleted")
            return file_change, commit_msg

        if change_split[0] == "renamed:":
            file_change = change_split[3].strip()
            commit_msg = await write_commit_message(file_change, "got renamed")
            return file_change, commit_msg

        else:
            raise ValueError(f"Invalid change: {change}")

    elif len(change_split) == 1:
        file_change = change_split[0].strip()
        commit_msg = await write_commit_message(file_change, "")
        return file_change, commit_msg
    else:
        raise ValueError(f"Invalid change: {change}")

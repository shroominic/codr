import asyncio as aio
from operator import itemgetter
from typing import Annotated, Literal

from funcchain import achain
from funcchain.schema.types import UniversalChatModel as LLM
from funcchain.syntax.params import Depends
from langchain_core.runnables import Runnable, RunnableLambda
from pydantic import BaseModel, Field
from rich import print

from ..shared.codebase.core import Codebase
from ..shared.schemas import Commit


async def exec_commit(Codebase: Codebase, llm: LLM, input: Commit) -> None:
    """commit command wrapper"""

    class GitChange(BaseModel):
        file: str = Field(description="Relative path to the file that got changed.")
        action: Literal["modified", "new", "deleted", "renamed"]
        diff: str | None = None

    async def _parse_change(Codebase: Codebase, git_status_line: str) -> GitChange:
        if len(change_split := git_status_line.split()) > 1:
            match change_split[0]:
                case "modified:":
                    return GitChange(
                        file=(file_change := change_split[1].strip()),
                        action="modified",
                        diff=await Codebase.shell(f"git diff --staged {file_change}"),
                    )

                case "new":
                    return GitChange(
                        file=(file_change := change_split[2].strip()),
                        action="new",
                        diff=await Codebase.shell(f"git diff --staged {file_change}"),
                    )

                case "deleted:":
                    return GitChange(
                        file=change_split[1].strip(),
                        action="deleted",
                    )

                case "renamed:":
                    return GitChange(file=change_split[3].strip(), action="renamed")

                case _:
                    raise ValueError(f"Invalid change: {change_split[0]}")

        elif len(change_split) == 1:
            return GitChange(file=change_split[0].strip(), action="new")

        else:
            raise ValueError(f"Invalid change: {change_split[0]}")

    parse_change: Runnable[dict, GitChange] = (
        itemgetter("git_status_line")
        | RunnableLambda(
            _parse_change,  # type: ignore
            name="parse_change",
        )
        | str
    )

    class GitCommit(BaseModel):
        message: str = Field(description="Commit message.")
        emoji: str = Field(description="Emoji to summarize the commit message.")
        changes: list[str] = Field(description="List of relative file paths this commit includes.")

        def __str__(self) -> str:
            return f"{self.emoji} {self.message}" + "".join(f"\n  - {change}" for change in self.changes) + "\n"

    async def write_commit(
        git_status_line: Annotated[str, Depends(parse_change)] = "",
    ) -> GitCommit:
        """
        Write a tiny commit message for these file changes.
        """
        return await achain(settings_override={"llm": llm})

    async def parse_changes(Codebase: Codebase, git_status_lines: list[str]) -> list[GitChange]:
        return [await _parse_change(Codebase, line) for line in git_status_lines]

    async def write_commits(git_changes: str) -> list[GitCommit]:
        """
        Write a list of git commit messages for all open changes.
        Group related changes together in a single commit (only if it makes sense).
        If a single commit message is too long, split it into multiple commits.
        """
        return await achain(settings_override={"llm": llm})

    async def commit_changes(Codebase: Codebase, stage: bool, auto_push: bool, no_group: bool) -> None:
        await Codebase.shell("git add .") if stage else None

        git_status = (await Codebase.shell("git status")).split("Changes not staged for commit:")[0]
        if "Changes to be committed" in git_status:
            git_status_lines = [c for c in git_status.split("\n") if c.startswith("\t")]

            if no_group:
                commit_tasks = [aio.create_task(write_commit(c)) for c in git_status_lines]
                for task in aio.as_completed(commit_tasks):
                    commit = await task
                    print(str(commit))
                    await Codebase.shell(f'git commit {commit.changes[0]} -m "{commit.emoji} {commit.message}"')
            else:
                git_changes = await parse_changes(Codebase, git_status_lines)
                for commit in await write_commits(str(git_changes)):
                    print(str(commit))
                    await Codebase.shell(f'git commit {" ".join(commit.changes)} -m "{commit.emoji} {commit.message}"')

            if auto_push:
                await Codebase.shell("git push")
        else:
            print("No changes to commit.\nUse --stage or -s to stage all open changes.")

    await commit_changes(Codebase, input.stage, input.push, input.no_group)

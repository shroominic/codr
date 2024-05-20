import asyncio
from typing import Annotated

from funcchain import Depends, chain, runnable
from funcchain.schema.types import UniversalChatModel as LLM
from funcchain.syntax import CodeBlock
from rich import print
from shared.codebase.clientio import show_yes_no_select
from shared.codebase.core import Codebase
from shared.codebase.tree import CodebaseTree
from shared.schemas import (
    CreatedFile,
    CreateDirectory,
    Debug,
    DeletedFile,
    FileChange,
    Implement,
    ModifiedFile,
    PlannedFileChange,
    PlannedFileChanges,
    Task,
)


async def exec_implement(codebase: Codebase, llm: LLM, input: Implement) -> None:
    """implement command wrapper"""

    @runnable(llm=llm)
    def plan_file_changes(
        goal: Task,
        codebase_tree: Annotated[CodebaseTree, Depends(codebase.tree.load)],
    ) -> PlannedFileChanges:
        """
        Which of these files from tree need to be modified to solve task?
        Answer with a list of file changes inside a JSON array.
        If you need to create a directory, use "mkdir" as method.
        Each file change consists of a path, method and description.
        Path is a relative path, make sure path is correct and file exists in codebase.
        """
        return chain()

    @runnable(llm=llm)
    def create_file_prompt(
        change: PlannedFileChange,
        codebase_tree: Annotated[CodebaseTree, Depends(codebase.tree.load)],
    ) -> CodeBlock:
        """
        Create a new file as part of solving the task.
        Reply with the complete file content.
        """
        return chain()

    @runnable(llm=llm)
    def modify_file_prompt(
        overall_task: Task,
        planned_file_change: PlannedFileChange,
        file_content: str,
        codebase_tree: Annotated[CodebaseTree, Depends(codebase.tree.load)],
    ) -> CodeBlock:
        """
        Modify this file using plan as part of solving main task.
        Do not change anything not related to goal/task, this includes formatting or comments.
        ONLY change what is described in the task.
        Rewrite entire file including changes, do not leave out any lines.
        """
        return chain()

    async def solve_task(
        codebase: Codebase,
        task_description: str,
        debug_cmd: str | None = None,
    ) -> None:
        # task_name = await summarize_task_to_name(task_description)
        # log(task_name)
        task = Task(description=task_description)

        # tree = await get_tree()

        # May result in more halluzinations
        # task.description = await improve_task_description(task, tree)
        # log("Improved task: ", task)

        changes, _ = await asyncio.gather(
            compute_changes(codebase, task),
            codebase.git.prepare_environment(task.description),
        )

        for change in changes:
            if isinstance(change, ModifiedFile):
                change.print_diff()
            else:
                print(change)

        if not await show_yes_no_select("Do you want to apply these changes?"):
            exit(0)

        await apply_changes(changes)

        if debug_cmd:
            print("DEBUGGING from debug_cmd:", debug_cmd)
            from .debug import exec_debug

            # command = gather_run_command(task)
            await exec_debug(
                codebase,
                llm,
                Debug(
                    command=debug_cmd,
                ),
            )

    async def compute_changes(
        codebase: Codebase,
        task: Task,
    ) -> list[FileChange]:
        planned_changes = await plan_file_changes.ainvoke({"goal": task})
        print("\nPlanned changes:\n", planned_changes)
        # if count_tokens(planned_changes.files) > 32:
        file_changes = await asyncio.gather(
            *[
                generate_change(
                    codebase=codebase,
                    task=task,
                    change=change,
                )
                for change in planned_changes.changes
            ]
        )
        return file_changes
        # else:
        #     file_changes = await generate_changes(task, planned_changes)
        #     log("\nFile changes:\n", file_changes)
        # return file_changes

    async def generate_change(
        codebase: Codebase,
        task: Task,
        change: PlannedFileChange,
    ) -> FileChange:
        # TODO: collect relevant context
        # TODO: plan file changes precise based on context
        if change.method == "create":
            return CreatedFile(
                relative_path=change.relative_path,
                content=(await create_file_prompt.ainvoke({"change": change})).code,
            )
        if change.method == "mkdir":
            return CreateDirectory(relative_path=change.relative_path)
        try:
            change.relative_path = await codebase.fix_file_path(
                change.relative_path,
            )
        except FileNotFoundError:
            return CreatedFile(
                relative_path=change.relative_path,
                content=(await create_file_prompt.ainvoke({"change": change})).code,
            )
        if change.method == "modify":
            return ModifiedFile(
                relative_path=change.relative_path,
                content=(
                    await modify_file_prompt.ainvoke(
                        {"overall_task": task, "planned_file_change": change, "file_content": change.content}
                    )
                ).code,
            )
        if change.method == "delete":
            return DeletedFile(
                relative_path=change.relative_path,
            )
        else:
            raise ValueError(f"Invalid method: {change.method}")

    async def apply_changes(
        changes: list[FileChange],
    ) -> None:
        for change in changes:
            if isinstance(change, CreateDirectory):
                await codebase.create_dir(change.relative_path)
            elif isinstance(change, CreatedFile):
                await codebase.create_file(change.relative_path, change.content)
            elif isinstance(change, ModifiedFile):
                await codebase.write_file(change.relative_path, change.content)
            elif isinstance(change, DeletedFile):
                await codebase.delete_file(change.relative_path)
            else:
                raise ValueError(f"Invalid change: {change}")

    async def generate_changes(
        task: Task,
        changes: PlannedFileChanges,
    ) -> list[FileChange]:
        """
        Generate file changes based on planned file changes
        """
        # gather file contents of all files of planned changes

        # merge into big prompt (with context)

        # generate changes based on prompt and output list of changes

        # return list of changes
        return []

    await solve_task(codebase, input.task, input.debug_cmd)

import asyncio

from funcchain import achain
from funcchain.schema.types import UniversalChatModel as LLM
from funcchain.syntax import CodeBlock
from rich import print

from ..shared.codebase.clientio import show_yes_no_select
from ..shared.codebase.core import Codebase
from ..shared.codebase.tree import CodebaseTree
from ..shared.schemas import (
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


async def exec_implement(Codebase: Codebase, llm: LLM, input: Implement) -> None:
    """implement command wrapper"""

    async def plan_file_changes(
        task: Task,
        Codebase_tree: CodebaseTree,
    ) -> PlannedFileChanges:
        """
        Which of these files from tree need to be modified to solve task?
        Answer with a list of file changes inside a JSON array.
        If you need to create a directory, use "mkdir" as method.
        Each file change consists of a path, method and description.
        Path is a relative path, make sure path is correct and file exists in Codebase.
        """
        return await achain(settings_override={"llm": llm})

    async def create_file_prompt(
        change: PlannedFileChange,
        Codebase_tree: CodebaseTree,
    ) -> CodeBlock:
        """
        PLAN:
        {change_description}

        FILE:
        {change_relative_path}

        Codebase_TREE:
        {Codebase_tree}

        Create a new file as part of solving the task.
        Reply with the file content.
        """
        return await achain(
            change_relative_path=change.relative_path,
            change_description=change.description,
            settings_override={"llm": llm},
        )

    async def modify_file_prompt(
        main_task: Task,
        Codebase_tree: CodebaseTree,
        change: PlannedFileChange,
    ) -> CodeBlock:
        """
        PLAN:
        {change_description}

        FILE:
        {change_content}

        Modify this file using plan as part of solving main task.
        Do not change anything not related to plan, this includes formatting or comments.
        Rewrite entire file including changes, do not leave out any lines.
        """
        return await achain(
            change_description=change.description,
            change_content=change.content,
            settings_override={"llm": llm},
        )

    async def solve_task(
        Codebase: Codebase,
        task_description: str,
        debug_cmd: str | None = None,
    ) -> None:
        # task_name = await summarize_task_to_name(task_description)
        # log(task_name)
        task = Task(
            description=task_description,
        )

        # tree = await get_tree()

        # May result in more halluzinations
        # task.description = await improve_task_description(task, tree)
        # log("Improved task: ", task)

        changes, _ = await asyncio.gather(
            compute_changes(Codebase, task),
            Codebase.git.prepare_environment(task.description),
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
                Codebase,
                llm,
                Debug(
                    command=debug_cmd,
                ),
            )

    async def compute_changes(
        Codebase: Codebase,
        task: Task,
    ) -> list[FileChange]:
        planned_changes = await plan_file_changes(task, await Codebase.tree.load())
        print("\nPlanned changes:\n", planned_changes)
        # if count_tokens(planned_changes.files) > 32:
        file_changes = await asyncio.gather(
            *[
                generate_change(
                    Codebase=Codebase,
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
        Codebase: Codebase,
        task: Task,
        change: PlannedFileChange,
    ) -> FileChange:
        # TODO: collect relevant context
        # TODO: plan file changes precise based on context
        tree = await Codebase.tree.load()
        if change.method == "create":
            return CreatedFile(
                relative_path=change.relative_path,
                content=(await create_file_prompt(change, tree)).code,
            )
        if change.method == "mkdir":
            return CreateDirectory(
                relative_path=change.relative_path,
            )
        try:
            change.relative_path = await Codebase.fix_file_path(change.relative_path)
        except FileNotFoundError:
            return CreatedFile(
                relative_path=change.relative_path,
                content=(await create_file_prompt(change, tree)).code,
            )
        if change.method == "modify":
            return ModifiedFile(
                relative_path=change.relative_path,
                content=(await modify_file_prompt(task, tree, change)).code,
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
                await Codebase.create_dir(change.relative_path)
            elif isinstance(change, CreatedFile):
                await Codebase.create_file(change.relative_path, change.content)
            elif isinstance(change, ModifiedFile):
                await Codebase.write_file(change.relative_path, change.content)
            elif isinstance(change, DeletedFile):
                await Codebase.delete_file(change.relative_path)
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

    await solve_task(Codebase, input.task, input.debug_cmd)

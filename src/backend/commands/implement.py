import asyncio

from funcchain import achain
from funcchain.syntax import CodeBlock

from ..codebase import CodeBase
from ..codebase.tree import CodeBaseTree
from ..schemas import (
    CreatedFile,
    CreateDirectory,
    DeletedFile,
    FileChange,
    ModifiedFile,
    PlannedFileChange,
    PlannedFileChanges,
    Task,
)

# from ..ui import show_yes_no_select


async def plan_file_changes(
    task: Task,
    codebase_tree: CodeBaseTree,
) -> PlannedFileChanges:
    """
    Which of these files from tree need to be modified to solve task?
    Answer with a list of file changes inside a JSON array.
    If you need to create a directory, use "mkdir" as method.
    Each file change consists of a path, method and description.
    path is a relative path, make sure path is
    correct and file exists in codebase.
    method is one of "create", "mkdir", "modify" or "delete".
    description is a compressed summary of knowledge describing what to change.
    """
    return await achain()


async def create_file_prompt(
    change: PlannedFileChange,
    codebase_tree: CodeBaseTree,
) -> CodeBlock:
    """
    PLAN:
    {change_description}

    FILE:
    {change_relative_path}

    Create a new file as part of solving task.
    Reply with the file content.
    """
    return await achain(
        change_relative_path=change.relative_path,
        change_description=change.description,
    )


async def modify_file_prompt(
    main_task: Task,
    codebase_tree: CodeBaseTree,
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
    )


async def implement_task(
    codebase: CodeBase,
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
        compute_changes(task, codebase),
        codebase.prepare_environment(task),
    )

    for change in changes:
        if isinstance(change, ModifiedFile):
            change.print_diff()
        else:
            print(change)

    # todo
    # if not await show_yes_no_select("Do you want to apply these changes?"):
    #     exit(0)

    await apply_changes(changes, codebase)

    if debug_cmd:
        print("DEBUGGING from debug_cmd:", debug_cmd)
        from .debug import auto_debug

        # command = gather_run_command(task)
        await auto_debug(codebase, debug_cmd, task.description, loop=True)


async def compute_changes(task: Task, codebase: CodeBase) -> list[FileChange]:
    planned_changes = await plan_file_changes(
        task,
        codebase_tree=await codebase.get_tree(),
    )
    print("\nPlanned changes:\n", planned_changes)
    # if count_tokens(planned_changes.files) > 32:
    file_changes = await asyncio.gather(
        *[
            generate_change(
                task=task,
                change=change,
                codebase=codebase,
            )
            for change in planned_changes.changes
        ]
    )
    return file_changes
    # else:
    #     file_changes = await generate_changes(task, planned_changes)
    #     log("\nFile changes:\n", file_changes)
    # return file_changes


async def generate_change(task: Task, change: PlannedFileChange, codebase: CodeBase) -> FileChange:
    # TODO: collect relevant context
    # TODO: plan file changes precise based on context
    tree = await codebase.get_tree()
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
        change.relative_path = await codebase.fix_file_path(change.relative_path)
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


async def apply_changes(changes: list[FileChange], codebase: CodeBase) -> None:
    for change in changes:
        if isinstance(change, CreateDirectory):
            await codebase.create_directory(change.relative_path)
        elif isinstance(change, CreatedFile):
            await codebase.create_file(change.relative_path, change.content)
        elif isinstance(change, ModifiedFile):
            await codebase.modify_file(change.relative_path, change.content)
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

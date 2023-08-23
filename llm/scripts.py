import asyncio
from codeio.codebase import CodeBase
from llm.schema import Task, PlannedFileChange, CreatedFile, ModifiedFile, DeletedFile, FileChange
from llm.chains import (
    improve_task_description,
    plan_file_changes,
    create_file,
    modify_file,
)


async def solve_task(task: Task, extra_info: str = "N/A") -> None:
    codebase = await CodeBase.load()
    tree = await codebase.get_tree()

    task = await improve_task_description(task, extra_info, tree)

    changes = (
        await asyncio.gather(
            compute_changes(task, codebase),
            codebase.prepare_environment(task),
        )
    )[0]

    await apply_changes(codebase, changes)


async def compute_changes(task: Task, codebase: CodeBase) -> list[FileChange]:
    planned_changes = await plan_file_changes(task, await codebase.get_tree())
    return await asyncio.gather(
        *[
            generate_change(
                task=task,
                change=change,
                codebase=codebase,
            )
            for change in planned_changes.changes
        ]
    )


async def generate_change(task: Task, change: PlannedFileChange, codebase: CodeBase) -> FileChange:
    # TODO: collect relevant context
    # TODO: plan file changes precise based on context
    tree = await codebase.get_tree()
    if change.method == "create":
        return CreatedFile(path=change.path, content=(await create_file(change, tree)).code)
    elif change.method == "modify":
        return ModifiedFile(path=change.path, changes=(await modify_file(change, tree)).changes)
    elif change.method == "delete":
        return DeletedFile(path=change.path)
    else:
        raise ValueError(f"Invalid method: {change.method}")


async def apply_changes(codebase: CodeBase, changes: list[FileChange]):
    for change in changes:
        if isinstance(change, CreatedFile):
            await codebase.create_file(change.path, change.content)
        elif isinstance(change, ModifiedFile):
            await codebase.change_file(change.path, change.changes)
        elif isinstance(change, DeletedFile):
            await codebase.delete_file(change.path)
        else:
            raise ValueError(f"Invalid change: {change}")

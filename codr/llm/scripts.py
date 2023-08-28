import asyncio

from codr.codebase.func import create_file, delete_file, fix_file_path, get_tree, modify_file, prepare_environment, bash
from codr.llm.chains import create_file_prompt, improve_task_description, modify_file_prompt, plan_file_changes, summarize_task_to_name, check_result, generate_task
from codr.llm.schema import CreatedFile, DeletedFile, FileChange, ModifiedFile, PlannedFileChange, Task
from funcchain.utils import log


async def solve_task(task_description: str) -> None:
    task_name = summarize_task_to_name(task_description)
    log("Task name:", task_name)
    task = Task(
        name=task_name,
        description=task_description,
    )
    
    tree = await get_tree()

    task.description = await improve_task_description(task, tree)
    log("Improved task: ", task)

    changes = (
        await asyncio.gather(
            compute_changes(task),
            prepare_environment(task),
        )
    )[0]

    await apply_changes(changes)
    
    # TODO: add auto_debug()

    
async def auto_debug() -> None:
    result = await bash("./test.sh")

    log("RESULT: ", result)

    if await check_result(result):
        return log("DEBUG SUCCESSFUL")

    description = await generate_task(result)
    log("TASK:", description)
    await solve_task(description)


async def compute_changes(task: Task) -> list[FileChange]:
    planned_changes = await plan_file_changes(task, await get_tree())
    log("Planned changes: ", planned_changes)
    return await asyncio.gather(
        *[
            generate_change(
                task=task,
                change=change,
            )
            for change in planned_changes.changes
        ]
    )


async def generate_change(task: Task, change: PlannedFileChange) -> FileChange:
    # TODO: collect relevant context
    # TODO: plan file changes precise based on context
    log("Generating change: ", change)
    change.relative_path = await fix_file_path(change.relative_path)
    tree = await get_tree()
    if change.method == "create":
        return CreatedFile(relative_path=change.relative_path, content=(await create_file_prompt(change, tree)).code)
    elif change.method == "modify":
        return ModifiedFile(
            relative_path=change.relative_path, content=(await modify_file_prompt(task, tree, change)).code
        )
    elif change.method == "delete":
        return DeletedFile(relative_path=change.relative_path)
    else:
        raise ValueError(f"Invalid method: {change.method}")


async def apply_changes(changes: list[FileChange]):
    for change in changes:
        log("Applying change: ", change)
        if isinstance(change, CreatedFile):
            await create_file(change.relative_path, change.content)
        elif isinstance(change, ModifiedFile):
            await modify_file(change.relative_path, change.content)
        elif isinstance(change, DeletedFile):
            await delete_file(change.relative_path)
        else:
            raise ValueError(f"Invalid change: {change}")

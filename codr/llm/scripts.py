import asyncio

from funcchain.utils.helpers import log  # type: ignore

from codr.codebase.func import (
    bash,
    create_directory,
    create_file,
    delete_file,
    fix_file_path,
    get_tree,
    modify_file,
    prepare_environment,
)
from codr.llm.chains import (
    check_desired_output,
    check_result,
    create_file_prompt,
    generate_task,
    improve_task_description,
    modify_file_prompt,
    plan_file_changes,
    summarize_task_to_name,
    write_commit_message,
)
from codr.llm.schema import CreatedFile, CreateDirectory, DeletedFile, FileChange, ModifiedFile, PlannedFileChange, Task


async def solve_task(
    task_description: str,
    debug_cmd: str | None = None,
) -> None:
    task_name = await summarize_task_to_name(task_description)
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

    log("Changes: ", changes)
    input("Press enter to apply changes.")

    await apply_changes(changes)

    if debug_cmd:
        # command = gather_run_command(task)
        await auto_debug(debug_cmd, task.description, loop=True)


async def auto_debug(
    command: str,
    goal: str | None = None,
    loop: bool = False,
) -> None:
    result = await bash(command)

    log("RESULT: ", result)

    if goal and await check_desired_output(result, goal) or not goal and await check_result(result):
        return log("DEBUG SUCCESSFUL")

    description = await generate_task(result, goal or "healthy")
    log("TASK:", description)
    await solve_task(description)

    if loop:
        await auto_debug(command, goal, loop)


async def compute_changes(task: Task) -> list[FileChange]:
    planned_changes = await plan_file_changes(task, await get_tree())
    log("\nPlanned changes:\n", planned_changes)
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
    tree = await get_tree()
    if change.method == "create":
        return CreatedFile(relative_path=change.relative_path, content=(await create_file_prompt(change, tree)).code)
    if change.method == "mkdir":
        return CreateDirectory(relative_path=change.relative_path)
    change.relative_path = await fix_file_path(change.relative_path)
    if change.method == "modify":
        return ModifiedFile(
            relative_path=change.relative_path, content=(await modify_file_prompt(task, tree, change)).code
        )
    if change.method == "delete":
        return DeletedFile(relative_path=change.relative_path)
    else:
        raise ValueError(f"Invalid method: {change.method}")


async def apply_changes(changes: list[FileChange]):
    for change in changes:
        log("Applying change: ", change)
        if isinstance(change, CreateDirectory):
            await create_directory(change.relative_path)
        elif isinstance(change, CreatedFile):
            await create_file(change.relative_path, change.content)
        elif isinstance(change, ModifiedFile):
            await modify_file(change.relative_path, change.content)
        elif isinstance(change, DeletedFile):
            await delete_file(change.relative_path)
        else:
            raise ValueError(f"Invalid change: {change}")


async def commit_changes() -> None:
    git_status = (await bash("git status")).split("Changes not staged for commit:")[0]
    if "Changes to be committed" in git_status:
        commits = await asyncio.gather(
            *[process_change(change) for change in git_status.split("\n") if change.startswith("\t")]
        )
        for change, msg in commits:
            await bash(f'git commit {change} -m "{msg}"')
            print("Committed: ", change, msg)


async def process_change(change: str) -> tuple[str, str]:
    change_split = change.split()
    if len(change_split) > 1:
        if change_split[0] == "modified:":
            file_change = change_split[1].strip()
            modifications = await bash(f"git diff {file_change}")
            commit_msg = await write_commit_message(file_change, modifications)
            return file_change, commit_msg
        if change_split[0] == "new":
            file_change = change_split[2].strip()
            modifications = await bash(f"git diff {file_change}")
            commit_msg = await write_commit_message(file_change, "")
            return file_change, commit_msg
        if change_split[0] == "deleted:":
            file_change = change_split[1].strip()
            commit_msg = await write_commit_message(file_change, "")
            return file_change, commit_msg
        else:
            raise ValueError(f"Invalid change: {change}")
    elif len(change_split) == 1:
        file_change = change_split[0].strip()
        commit_msg = await write_commit_message(file_change, "")
        return file_change, commit_msg
    else:
        raise ValueError(f"Invalid change: {change}")

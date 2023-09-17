from funcchain.chain import achain
from funcchain.parser import CodeBlock

from codr.codebase.tree import CodeBaseTree
from codr.llm.schema import PlannedFileChange, PlannedFileChanges, Task


async def summarize_file(content: str) -> str:
    """
    FILE CONTENT:
    {content}

    Summarize file content.
    Try to describe file in a way that a programmer can understand it without reading code.
    Make it fit in one line but don't be afraid to use multiple sentences.
    """
    return await achain()


async def search_important_files(task: Task, tree: CodeBaseTree) -> list[str]:
    """
    TASK:
    {task}

    CODEBASE TREE:
    {tree}

    Which of these files are important to understand and solve task?
    """
    return await achain()


async def fix_filename(file_name: str, tree: CodeBaseTree) -> str:
    """
    RELATIVE_FILE_PATH:
    {file_name}

    CODEBASE TREE:
    {tree}

    Fix RELATIVE_FILE_PATH to match
    valid relative file path from CodeBaseTree.
    """
    return await achain()


async def plan_file_changes(task: Task, tree: CodeBaseTree) -> PlannedFileChanges:
    """
    TASK:
    {task}

    CODEBASE TREE:
    {tree}

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


async def generate_file_change(file_name: str, abstract_plan: str, tree: CodeBaseTree) -> str:
    """
    FILE:
    {file_name}

    CODEBASE TREE:
    {tree}

    ABSTRACT PLAN:
    {abstract_plan}

    Generate a precise plan for file change.
    Answer with a compressed summary of knowledge describing what to change.
    """
    return await achain()


async def create_file_prompt(change: PlannedFileChange, tree: CodeBaseTree) -> CodeBlock:
    """
    FILE:
    {change_relative_path}

    CODEBASE TREE:
    {tree}

    PLAN:
    {change_description}

    Create a new file as part of solving task.
    Reply with the file content.
    """
    return await achain(
        change_relative_path=change.relative_path,
        change_description=change.description,
    )


async def modify_file_prompt(task: Task, tree: CodeBaseTree, change: PlannedFileChange) -> CodeBlock:
    """
    CODEBASE TREE:
    {tree}

    MAIN TASK:
    {task}

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

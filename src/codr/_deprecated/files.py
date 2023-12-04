from funcchain import achain

from ..codebase.tree import CodeBaseTree
from ..schema import Task


async def summarize_file(content: str) -> str:
    """
    Summarize file content.
    Try to describe file in a way that a programmer can understand it without reading code.
    Make it fit in one line but don't be afraid to use multiple sentences.
    Do not use filler words and create a really dense piece of information.
    """
    return await achain()


async def search_important_files(task: Task, codebase_tree: CodeBaseTree) -> list[str]:
    """
    Which of these files are important to understand and solve task?
    """
    return await achain()


async def fix_filename(relative_file_path: str, codebase_tree: CodeBaseTree) -> str:
    """
    Fix RELATIVE_FILE_PATH to match
    valid relative file path from CodeBaseTree.
    """
    return await achain()


async def generate_file_change(
    file_name: str, abstract_plan: str, codebase_tree: CodeBaseTree
) -> str:
    """
    Generate a precise plan for file change.
    Answer with a compressed summary of knowledge describing what to change.
    """
    return await achain()

from funcchain import achain

from ...shared.schemas import Task
from ..codebase.tree import CodeBaseTree


async def improve_task_description(
    task: Task,
    codebase_tree: CodeBaseTree,
) -> str:
    """
    Improve task description based on context of codebase.
    Create a dense piece of knowledge giving understanding of task/goal.
    Write it for a programmer with only access to a part of codebase.
    """
    return await achain()


async def summarize_task_to_name(
    task_description: str,
) -> str:
    """
    Summarize task in less than 5 words to create a name for it.
    Only reply with this name.
    """
    return await achain()

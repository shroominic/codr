from codr.codebase.tree import CodeBaseTree
from codr.llm.schema import Task
from funcchain.parser import LambdaOutputParser
from funcchain.shortcuts import afuncchain


async def improve_task_description(task: Task, tree: CodeBaseTree) -> str:
    """
    CODEBASE TREE:
    {tree}

    TASK DESCRIPTION:
    {task}

    Improve task description based on context of codebase.
    Create a dense piece of knowledge giving understanding of task/goal.
    Write it for a programmer with only access to a part of codebase.
    """
    return await afuncchain()


async def ask_additional_question(task: Task) -> str | None:
    """
    TASK: {task.name}
    {task.description}

    This is task you are supposed to solve.
    Evaluate if task is clear or if you have additional questions.
    Ask your question(s) or just answer 'Clear!'.
    """
    return await afuncchain(
        parser=LambdaOutputParser(
            _parse=lambda t: t if "clear" not in t.lower() else None,
        )
    )


async def summarize_task_to_name(task_description: str) -> str:
    """
    TASK:
    {task_description}

    Summarize task in less than 5 words to create a name for it.
    Only reply with this name.
    """
    return await afuncchain()


async def generate_task(result: str) -> str:
    """
    CONSOLE OUTPUT:
    {result}

    Generate a task description to fix the error.
    """
    return await afuncchain()

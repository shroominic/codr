from rich import print

from pydantic import BaseModel
from funcchain import achain
from ..codebase.func import (
    get_tree,
    read_file,
)
from ..codebase.tree import CodeBaseTree


class RelevantFiles(BaseModel):
    relevant_files: list[str]


async def get_relevant_files(
    user_question: str,
    codebase_tree: CodeBaseTree,
) -> RelevantFiles:
    """
    Which files are most relevant to answer the user question?
    Extract max 7 relevant relative file paths from the codebase tree.
    Create a list containing relevant_files as strings.
    If no files are relevant, return an empty list.
    """
    return await achain()


async def codebase_answer(
    question: str,
    codebase_tree: CodeBaseTree,
    knowledge: list[str] = ["N/A"],
) -> str:
    """
    Answer the question based on the codebase and context.
    Format your answer in a way that is easy to read inside a terminal.
    You can utilize python rich format features.
    """
    return await achain()


async def expert_answer(question: str) -> str:
    # classify: check if question requires expert answer
    tree = await get_tree()
    knowledge: list[str] = []

    paths = (await get_relevant_files(question, tree)).relevant_files
    print("👀 reading files:", paths)
    for path in paths:
        knowledge.append(await read_file(path))

    return await codebase_answer(question, tree, knowledge)

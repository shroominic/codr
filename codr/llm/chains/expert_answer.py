from funcchain import achain
from langchain.pydantic_v1 import BaseModel

from ...codebase.tree import CodeBaseTree


class RelevantFiles(BaseModel):
    relevant_files: list[str]


async def get_relevant_files(
    user_question: str,
    codebase_tree: CodeBaseTree,
) -> RelevantFiles:
    """
    Which files are most relevant to answer the user question?
    Extract all relevant relative file paths from the codebase tree.
    Create a list containing relevant_files as strings. If no files are relevant, return an empty list.
    """
    return await achain()


async def codebase_answer(
    question: str,
    codebase_tree: CodeBaseTree,
    knowledge: list[str] = ["N/A"],
) -> str:
    """
    Answer the question based on the codebase and context.
    """
    return await achain()

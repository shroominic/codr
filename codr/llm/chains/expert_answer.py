from funcchain.chain import achain

from langchain.pydantic_v1 import BaseModel, Field

from codr.codebase.tree import CodeBaseTree


class RelevantFiles(BaseModel):
    relevant_files: list[str]


async def get_relevant_files(question: str, tree: CodeBaseTree) -> RelevantFiles:
    """
    USER QUESTION:
    {question}
    
    CODEBASE TREE:
    {tree}

    Which files are most relevant to answer the user question?
    Extract all relevant relative file paths from the codebase tree.
    Create a list containing relevant_files as strings. If no files are relevant, return an empty list.
    """
    return await achain()


async def codebase_answer(question: str, tree: CodeBaseTree, knowledge: list[str] = ["N/A"]) -> str:
    """
    QUESTION: {question}

    CODEBASE STRUCTURE:
    {tree}

    CONTEXT:
    {knowledge}

    Answer the question based on the codebase and context.
    """
    return await achain()

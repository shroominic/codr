from rich import print

from pydantic import BaseModel, field_validator
from funcchain import achain
from ..codebase.func import (
    get_tree,
    read_file,
    file_exists,
)
from ..codebase.tree import CodeBaseTree


class RelevantFiles(BaseModel):
    relevant_files: list[str]

    @field_validator("relevant_files")
    def check_relevant_files(cls, v: list[str]) -> list[str]:
        if len(v) > 7:
            raise ValueError("Too many files")
        for path in v:
            if not file_exists(path):
                raise ValueError(f"FilePath does not exist in Codebase: {path}")
        return v


async def get_relevant_files(
    user_question: str,
    codebase_tree: CodeBaseTree,
) -> RelevantFiles:
    """
    Which files are most relevant to answer the user question?
    return ONLY the relevant relative paths, produce the MINIMUM neccesary up to a MAXIMUM OF 7.
    Create a list containing relevant_files as strings.
    If no files are relevant, return an empty list.
    """
    return await achain()


async def codebase_answer(
    question: str,
    codebase_tree: CodeBaseTree,
    relevant_files: list[str] = ["N/A"],
) -> str:
    """
    Answer the question based on the codebase tree and relevant files.
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

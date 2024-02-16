from asyncio import gather
from typing import Annotated

from funcchain import chain, runnable
from funcchain.syntax.params import Depends
from rich import print
from rich.markdown import Markdown

from ..codebase.func import get_tree, read_file
from ..codebase.tree import CodeBaseTree


async def aload_files(paths: list[str]) -> list[str]:
    return await gather(*[read_file(path) for path in paths])


@runnable
def get_relevant_files(
    question: str,
    codebase_tree: Annotated[CodeBaseTree, Depends(get_tree)],
) -> list[str]:
    """
    Which files are most relevant to answer the user question?
    Return a list of strings with ONLY the relevant relative paths,
    Do not include unrelated files and keep the list short.
    If no files are relevant, respond with an empty list.
    """
    return chain()


@runnable
def codebase_answer(
    question: str,
    codebase_tree: Annotated[CodeBaseTree, Depends(get_tree)],
    relevant_files: Annotated[str, Depends(get_relevant_files | aload_files | str)],
) -> str:
    """
    Answer the question based on the codebase tree and relevant files.
    """
    return chain()


async def expert_answer(question: str) -> str:
    answer = ""
    async for chunk in codebase_answer.astream({"question": question}):
        answer += chunk
        print("\033c", end="\n")
        print(Markdown(answer))

    return answer

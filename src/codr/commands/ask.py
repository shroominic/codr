from asyncio import gather
from typing import Annotated

from funcchain import chain, runnable
from funcchain.schema.types import UniversalChatModel as LLM
from funcchain.syntax.params import Depends
from rich import print
from rich.markdown import Markdown
from shared.codebase.core import Codebase
from shared.codebase.tree import CodebaseTree
from shared.schemas import AskCodebase


async def exec_ask(codebase: Codebase, llm: LLM, input: AskCodebase) -> None:
    """ask Codebase command wrapper"""

    async def aload_files(paths: list[str]) -> list[str]:
        return await gather(*[codebase.read_file(path) for path in paths])

    @runnable(llm=llm)
    def get_relevant_files(
        question: str,
        codebase_tree: Annotated[CodebaseTree, Depends(codebase.tree.load)],
    ) -> list[str]:
        """
        Which files are most relevant to answer the user question?
        Return a list of strings with ONLY the relevant relative paths,
        Do not include unrelated files and keep the list short.
        If no files are relevant, respond with an empty list.
        """
        return chain()

    @runnable(llm=llm)
    def codebase_answer(
        question: str,
        codebase_tree: Annotated[CodebaseTree, Depends(codebase.tree.load)],
        relevant_files: Annotated[str, Depends(get_relevant_files | aload_files | str)],
    ) -> str:
        """
        Answer the question based on the Codebase tree and relevant files.
        """
        return chain()

    async def expert_answer(question: str) -> str:
        answer = ""
        async for chunk in codebase_answer.astream({"question": question}):
            answer += chunk
            print("\033c", end="\n")
            print(Markdown(answer))

        return answer

    await expert_answer(input.question)

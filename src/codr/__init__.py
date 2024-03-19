from funcchain.schema.types import UniversalChatModel as LLM
from shared.codebase.core import Codebase
from shared.schemas.actions import AskCodebase, Commit, Debug, Implement, Shell

from . import commands


class Codr:
    def __init__(self, codebase: Codebase, llm: LLM) -> None:
        self.codebase = codebase
        self.llm = llm

    async def implement(self, task: str, debug_cmd: str | None = None) -> None:
        await commands.exec_implement(
            self.codebase,
            self.llm,
            Implement(task=task, debug_cmd=debug_cmd),
        )

    async def debug(self, command: str, goal: str, focus: str | None = None, loop: bool = False) -> None:
        await commands.exec_debug(
            self.codebase,
            self.llm,
            Debug(command=command, goal=goal, focus=focus, loop=loop),
        )

    async def commit(self, stage: bool = False, push: bool = False, no_group: bool = False) -> None:
        await commands.exec_commit(
            self.codebase,
            self.llm,
            Commit(stage=stage, push=push, no_group=no_group),
        )

    async def shell(self, instruction: str, auto_execute: bool = False) -> None:
        await commands.exec_shell(
            self.codebase,
            self.llm,
            Shell(instruction=instruction),
        )

    async def ask(self, question: str) -> None:
        await commands.exec_ask(
            self.codebase,
            self.llm,
            AskCodebase(question=question),
        )

    async def chat(self, instruction: str = "") -> None:
        if instruction:
            await commands.dynamic_request(
                self.codebase,
                self.llm,
                instruction,
            )
        else:
            instruction = input("\nInstruction:\n> ")
            await commands.dynamic_request(
                self.codebase,
                self.llm,
                instruction,
            )

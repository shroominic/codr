from funcchain import achain
from funcchain.syntax import CodeBlock

from ..codebase.tree import CodeBaseTree
from ..schema import Task


async def generate_code_summary(
    task: Task,
    codebase_tree: CodeBaseTree,
) -> str:
    """
    Summarize codebase, answer with a compressed piece of knowledge.
    What technologies and frameworks are used? What is general structure?
    Write it as context for a programmer with only access to a small part of codebase.
    """
    return await achain()


async def query_relevant_context(
    task: Task,
    codebase_tree: CodeBaseTree,
    file_modifications: dict,
    file_name: str,  # TODO: fix
    abstract_plan: str,
) -> str:
    """
    CODEBASE SUMMARY:  # TODO: fix
    {code_summary}

    MODIFICATIONS:
    {modifications}

    Query relevant context for each file.
    Relevant context is information that is needed to plan precise changes.
    """
    return await achain()


async def llm_format(
    file: str,
) -> CodeBlock:
    """
    Rewrite following file to match proper formatting.
    Do not change code or contents, only appearance.
    If file is already properly formatted, return same file.
    """
    return await achain()


async def gather_test_cmd(
    codebase_tree: CodeBaseTree,
) -> CodeBlock:
    """
    Gather command to test codebase.
    There might be a script to run tests,
    or you need to run them manually.
    Reply with a bash codeblock containing command.
    """
    return await achain()

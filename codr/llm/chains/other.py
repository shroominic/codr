from codr.llm.schema import Task
from codr.codebase.tree import CodeBaseTree
from funcchain.parser import CodeBlock
from funcchain.shortcuts import afuncchain


async def generate_code_summary(task: Task, tree: CodeBaseTree) -> str:
    """
    CODEBASE TREE:
    {tree}

    Summarize codebase, answer with a compressed piece of knowledge.
    What technologies and frameworks are used? What is general structure?
    Write it as context for a programmer with only access to a small part of codebase.
    """
    return await afuncchain()


async def query_relevant_context(
    task: Task,
    tree: CodeBaseTree,
    file_modifications: dict,
    file_name: str,
    abstract_plan: str,
) -> str:
    """
    TASK:
    {task}

    CODEBASE TREE:
    {tree}

    CODEBASE SUMMARY:
    {code_summary}

    MODIFICATIONS:
    {modifications}

    ABSTRACT PLAN:
    {abstract_plan}

    Query relevant context for each file.
    Relevant context is information that is needed to plan precise changes.
    """
    return await afuncchain()


async def llm_format(file: str):
    """
    FILE:
    {file}

    Rewrite following file to match proper formatting.
    Do not change code or contents, only appearance.
    If file is already properly formatted, return same file.
    Reply with a codeblock containing formatted file.
    """
    return await afuncchain()


async def gather_test_cmd(tree: CodeBaseTree) -> CodeBlock:
    """
    CODEBASE TREE:
    {tree}

    Gather command to test codebase.
    There might be a script to run tests,
    or you need to run them manually.
    Reply with a bash codeblock containing command.
    """
    return await afuncchain()

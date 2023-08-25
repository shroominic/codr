from codeio.tree import CodeBaseTree
from funcchain.shortcuts import funcchain, afuncchain
from funcchain.parser import LambdaOutputParser, CodeBlock, ParserBaseModel
from llm.schema import Task, PlannedFileChanges, PlannedFileChange, CreatedFile
from pydantic import Field


def ask_additional_question(task: Task) -> str | None:
    """
    TASK: {task.name}
    {task.description}

    This is the task you are supposed to solve.
    Evaluate if the task is clear or if you have additional questions.
    Ask your question(s) or just answer 'Clear!'.
    """
    return funcchain(
        parser=LambdaOutputParser(
            _parse=lambda t: t if "clear" not in t.lower() else None,
        )
    )


def summarize_task_to_name(task_description: str) -> str:
    """
    TASK:
    {task_description}

    Summarize the task in less than 5 words to create a name for it.
    Only reply with this name.
    """
    return funcchain()


async def summarize_file(content: str) -> str:
    """
    FILE CONTENT:
    {content}

    Summarize the file content.
    Try to describe the file in a way that a programmer can understand it without reading the code.
    Make it fit in one line but don't be afraid to use multiple sentences.
    """
    return await afuncchain()


async def search_important_files(task: Task, tree: CodeBaseTree) -> list[str]:
    """
    TASK:
    {task}

    CODEBASE:
    {tree}

    Which of these files are important to understand and solve the task?
    """
    return await afuncchain()


async def generate_code_summary(task: Task, tree: CodeBaseTree) -> str:
    """
    CODEBASE:
    {tree}

    Summarize the codebase, answer with a compressed piece of knowledge. What technologies and frameworks are used? What is the general structure?
    Write it as context for a programmer with only access to a small part of the codebase.
    """
    return await afuncchain()


async def improve_task_description(task: Task, extra_info: str, tree: CodeBaseTree) -> Task:
    """
    CODEBASE:
    {tree}

    TASK:
    {task}

    ADDITIONAL INFO:
    {extra_info}

    Improve the task description based on the context of the codebase.
    Create a dense piece of knowledge giving understanding of the task/goal.
    Write it for a programmer with only access to a part of the codebase.
    """
    return await afuncchain()


async def plan_file_changes(task: Task, tree: CodeBaseTree) -> PlannedFileChanges:
    """
    TASK:
    {task}

    CODEBASE:
    {tree}

    Which of these files from the tree need to be modified to solve the task?
    Answer with a list of file changes inside a JSON array.
    Each file change consists of a path, method and description.
    The path is a relative path, make sure the path is
    correct and the file exists in the codebase.
    The method is one of "create", "modify" or "delete".
    The description is a compressed summary of knowledge describing what to change.
    """
    return await afuncchain()


async def generate_file_change(file_name: str, abstract_plan: str, tree: CodeBaseTree) -> str:
    """
    FILE:
    {file_name}

    CODEBASE:
    {tree}

    ABSTRACT PLAN:
    {abstract_plan}

    Generate a precise plan for the file change.
    Answer with a compressed summary of knowledge describing what to change.
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

    Rewrite the following file to match proper formatting.
    Do not change the code or contents, only the appearance.
    If the file is already properly formatted, return the same file.
    Reply with a codeblock containing the formatted file.
    """
    return await afuncchain()


async def create_file(change: PlannedFileChange, tree: CodeBaseTree) -> CodeBlock:
    """
    FILE:
    {change.relative_path}

    CODEBASE:
    {tree}

    PLAN:
    {change.description}

    Create a new file as part of solving the task.
    Reply with a codeblock containing the code to create the file.
    """
    return await afuncchain()


class FileModifications(ParserBaseModel):
    changes: list[tuple[int, str, str]]

    @staticmethod
    def format_instructions() -> str:
        return """
            Create list called "changes",
            containing smaller lists: [line_number, action, "new code"].
            Action can be one of the following:
            - add: insert new code at line number and shift following lines down
            - overwrite: replace line number with new code
            - delete: remove code at line number
            
            Format these changes as json codeblock:
            
            ```json
            {{
                // (line_number, 'action', 'new code')
                "changes": [
                    [0, "add", "import example"],
                    [4, "overwrite", "def foo():"],
                    [5, "add", "    print(\"hello world\")"],
                    [6, "delete", "    print(\"bar\")"]
                    // ... and so on
                ]
            }}
            ```
            """


async def modify_file(task: Task, tree: CodeBaseTree, change: PlannedFileChange) -> CodeBlock:
    """
    CODEBASE:
    {tree}

    MAIN TASK:
    {task}

    PLAN:
    {change_description}

    FILE:
    {change_content}

    Modify this file using the plan as part of solving the main task.
    Do not change anything not related to the plan, this includes formatting or comments.
    Rewrite the entire file including the changes, do not leave out any lines.
    """
    return await afuncchain(
        change_description=change.description,
        change_content=change.content,
    )

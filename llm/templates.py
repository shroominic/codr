from langchain.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.schema import SystemMessage

default_system = SystemMessage(
    content="You are a coding assistant solving tasks for developers." "Be advanced and precise in your responses.",
)


solve_task_system_instruction = SystemMessage(
    content="""
You are a coding assistant solving tasks for developers.
To solve the task you get an abstract description of the codebase and the task.
The final goal is to solve the task by doing the necessary changes to the codebase.
To get there you the developer guides you through the process in a conversation.
If you need more information about the codebase or the task you can ask the developer.
For hard tasks it can be helpful to first write down a plan step by step.
Be precise in your responses and communicate like an efficient expert.
"""  # TODO: handle questions as queries -> inject context
)


important_files = HumanMessagePromptTemplate.from_template(
    template="""
Which files are important to read for gaining understanding of the codebase?

Codebase:
{code_tree}

For example in a python project you might want to look at the 'requirements.txt' file
to understand which technologies are used in the project.\n
Reply like this and make sure pathes are in 'single quotes' and not "double quotes":

```json
{{
    "relevant_files": [
        "path/to/file1.txt",
        "path/to/file2.js",
        // ... and so on
        // but choose wisely: max 4 files
    ]
}}
```
"""
)

repo_summary = HumanMessagePromptTemplate.from_template(
    template="Summarize what this repository is about and what it does.\n"
    "Repository name: {repo_name}\n"
    "Repository description: {repo_description}\n"
    "Repository keywords: {repo_keywords}\n"
    "Repository codebase: \n{code_tree}\n"
    "Relevant files: \n{relevant_files}\n\n"
    "Describe the technologies used and the structure of the codebase. "
    "Please be as detailed and precise as possible but keep it short.\n"
)

issue_summary = HumanMessagePromptTemplate.from_template(
    template="Repository Summary: \n{repo_summary}\n"
    "Issue title: {issue_title}\n"
    "Issue description: {issue_description}\n"
    "Describe step by step (abstract) how to implement the issue and what files are relevant. "
    "Be precise and keep it short.\n"
)


prepare_changes = HumanMessagePromptTemplate.from_template(
    template="""
Repository codebase:
{code_tree}
Repository description:
{repo_summary}
Issue description:
{issue_summary}

What files need to be changed to solve the issue?
What new files need to be created?

Write paths using 'single quotes'.
Make sure to put only file paths that exist in the codebase/project directory in files_to_change.
Respond with a codeblock like this:

```json
{{
    "new_files": [
        "path/to/new_file1.py",
        "path/to/new_file2.ipynb",
        // ... and so on
    ],
    "change_files": [
        "path/to/file1.txt",
        "path/to/file2.js",
        // ... and so on
    ]
}}
```
"""
)

new_file = HumanMessagePromptTemplate.from_template(
    template="""
Repository description:
{repo_summary}

Issue description:
{issue_summary}

Implement this file {file_path} to solve the issue.
After completion this the file will be created and added to the codebase.
Reply with a codeblock containing the content of the new file.
"""
)

change_file = HumanMessagePromptTemplate.from_template(
    template="""
Repository description:
{repo_summary}
Issue description:
{issue_summary}
First write a detailed instruction on how to change the file {file_path}.

# [Begin file content]
{file_content}
# [Eind file content]

Then create a list called "changes".
This list should contain tuples of the form (line_number, action, "new code").
Action can be one of the following:
- add: insert a new line of code at the line with the given number and shift all following lines down
- overwrite: overwrite the line with the given number
- delete: delete the line with the given number

Write down all changes and
reply with a codeblock like this:
        # (line_number, 'action', 'new code')
```json
{{
    "changes": [
        [0, "add", "import newexample"],
        [4, "overwrite", "def foo():"],
        [5, "add", "    print(\"hello world\")"],
        [6, "delete", "    print(\"bar\")"]
        // ... and so on
    ]
}}
```
"""
)

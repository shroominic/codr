import re, os
import asyncio
import subprocess
from datetime import datetime
from typing import AsyncGenerator, Generator
from pathlib import Path
from codr.tree import CodeBaseTree
from codr.llm.schema import Task


class CodeBase:
    def __init__(self, tree: CodeBaseTree | None = None):
        self.tree = tree

    @classmethod
    async def load(cls) -> "CodeBase":
        tree = await CodeBaseTree.load()
        return cls(tree)

    async def _bash(self, *commands: str) -> AsyncGenerator[bytes, None]:
        """
        Run a bash command
        """
        process = await asyncio.create_subprocess_shell(
            "\n".join(commands),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if stdout:
            yield stdout
        if stderr:
            yield stderr

    async def bash(self, *commands: str) -> AsyncGenerator[str, None]:
        """
        Run a bash command
        """
        async for output in self._bash(*commands):
            yield output.decode()
            
    def bash_sync(self, *commands: str) -> Generator[str, None, None]:
        """
        Run a bash command
        """
        process = subprocess.Popen(
            "\n".join(commands),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        if stdout:
            yield stdout.decode()
        if stderr:
            yield stderr.decode()

    async def bash_str(self, *commands: str) -> str:
        """
        Run a bash command
        """
        summed_output = ""
        async for output in self.bash(*commands):
            summed_output += output
        return summed_output
    
    def bash_str_sync(self, *commands: str) -> str:
        """
        Run a bash command
        """
        summed_output = ""
        for output in self.bash_sync(*commands):
            summed_output += output
        return summed_output

    async def read_file(self, path: Path) -> AsyncGenerator[bytes, None]:
        """
        Read a file from the codebase
        """
        async for output in self._bash(f"cat {path}"):
            yield output
            
    def read_file_sync(self, path: Path) -> str:
        """
        Read a file from the codebase
        """
        with open(path) as f:
            return f.read()

    async def show_tree(self) -> str:
        """
        Show the codebase tree
        """
        if self.tree is None:
            self.tree = await CodeBaseTree.load()
        return self.tree.show()
    
    def show_tree_sync(self) -> str:
        """
        Show the codebase tree
        """
        if self.tree is None:
            self.tree = asyncio.run(CodeBaseTree.load())
        return self.tree.show()

    async def get_tree(self) -> CodeBaseTree:
        """
        Get the codebase tree
        """
        if self.tree is None:
            self.tree = await CodeBaseTree.load()
        return self.tree
    
    def get_tree_sync(self) -> CodeBaseTree:
        """
        Get the codebase tree
        """
        if self.tree is None:
            self.tree = asyncio.run(CodeBaseTree.load())
        return self.tree

    # TODO: test this
    async def file_exists(self, relative_path: Path) -> bool:
        """
        Check if a file exists
        """
        return os.path.isfile(relative_path)

    # TODO test this
    async def validate_file_paths(self, file_paths) -> bool:
        """
        Check if file paths are valid
        """
        return bool((all([re.search(r".*\\..*", path) is not None for path in {file_paths}])))

    # TODO: make async
    async def create_file(self, relative_path: str, content: str):
        """
        Create a file in the codebase
        """
        with open(relative_path, "w") as f:
            f.write(content)

    # TODO: test this
    # async def change_file(self, relative_path: str, changes: list[tuple[int, str, str]]) -> None:
    #     """
    #     Change a file in the codebase
    #     """
    #     async for output in self.bash(f"cat {relative_path}"):
    #         file_content = output
    #         lines = file_content.split("\n")
    #         for line_number, action, new_code in changes:
    #             if action == "add":
    #                 lines.insert(line_number, "\n" + new_code)
    #             elif action == "overwrite":
    #                 lines[line_number] = new_code + "\n"
    #             elif action == "delete":
    #                 del lines[line_number]
    #         file_content = "\n".join(lines)
    #         await self.bash_str(f"echo '{file_content}' > {relative_path}")
    #         await self.bash_str(f"black {relative_path}")

    async def change_file(self, relative_path: str, content: str) -> None:
        """
        Replace a file in the codebase
        """
        import aiofiles  # type: ignore
        
        async with aiofiles.open(relative_path, "w") as f:
            await f.write(content)
        await self.bash_str(f"black {relative_path}")

    async def delete_file(self, relative_path: str) -> None:
        await self.bash_str(f"rm ./{relative_path}")

    async def prepare_environment(self, task: Task) -> None:
        """
        Prepare the git env for the codebase
        """
        # if there are open changes stash them
        git_status = await self.bash_str("git status")
        if "Changes not staged for commit" in git_status:
            stash_result = await self.bash_str("git stash")
            if "No local changes to save" in stash_result:
                print("No changes to stash")
            elif "Saved working directory and index state" not in stash_result:
                raise Exception(f"Failed to stash changes: {stash_result}")

        # checkout to new created branch with task name
        task_name = task.name.replace(" ", "_") + "_" + datetime.now().strftime("%Y%m%d%H%M%S")
        checkout_result = await self.bash_str(f"git checkout -b {task_name}")
        if "Switched to a new branch" not in checkout_result:
            raise Exception(f"Failed to checkout to new branch: {checkout_result}")

        # apply stash to new branch
        apply_result = await self.bash_str("git stash apply")

    async def fix_file_path(self, relative_path: str) -> str:
        """Fix file name to absolute path"""
        tree = await self.get_tree()
        file_name = relative_path.split("/")[-1]
        files = [
            file for file in tree.files 
            if file.name.split("/")[-1] == file_name
        ]
        
        if len(files) > 1:
            raise Exception(f"Duplicate file name: {file_name}, {files}")
        elif len(files) < 1:
            raise Exception(f"File not found: {file_name}, {files}")
        
        return files[0].name
            

import asyncio
import fnmatch
import hashlib
import os
from pathlib import Path
from typing import Any, Union

import yaml  # type: ignore
from pydantic.v1 import BaseModel

IGNORED: set[str] = {
    ".context",
    ".git",
    "node_modules",
    "__pycache__",
    "venv",
    "poetry.lock",
    "package-lock.json",
    "yarn.lock",
    ".mypy_cache",
    ".pytest_cache",
    ".vscode",
    ".idea",
    ".DS_Store",
    "*.pyc",
    "Cargo.lock",
}


def load_gitignore() -> None:
    """
    Loads the patterns from .gitignore and updates the global IGNORED set.
    """
    gitignore_files = [file for file in Path(".").rglob(".gitignore")]
    for gitignore_file in gitignore_files:
        with open(gitignore_file, "r") as f:
            for line in f.readlines():
                pattern = line.strip().split("#")[0]
                if pattern and pattern != "*":
                    pattern = pattern.removesuffix("/")
                    IGNORED.add(pattern)


load_gitignore()


def is_ignored_by_gitignore(file_path: str) -> bool:
    """
    Checks if a file is ignored by .gitignore
    """
    return any(
        fnmatch.fnmatch(file_path, pattern)
        or fnmatch.fnmatch(os.path.basename(file_path), pattern)
        for pattern in IGNORED
    )


class CodeBaseNode(BaseModel):
    name: str
    sha256: str
    embedding: list[float] | None = None

    @property
    def path(self) -> Path:
        return Path(".") / self.name

    @path.setter
    def path(self, value: Union[str, Path]) -> None:
        self.name = Path(value).relative_to(Path.cwd()).as_posix()

    def __str__(self, indent: int = 0) -> str:
        return " " * indent + f"Node: {self.path.name}"


class CodeBaseFile(CodeBaseNode):
    summary: str

    def __init__(self, path: Path | str, **data: Any) -> None:
        data["name"] = Path(path).as_posix()
        super().__init__(**data)

    @classmethod
    def from_dict(cls, data: dict) -> "CodeBaseFile":
        path = data.pop("name")
        return cls(path, **data)

    @classmethod
    async def from_path(cls, path: Path) -> "CodeBaseFile":
        from ..llm.chains.files import summarize_file

        try:
            content = path.read_text()
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            summary = await summarize_file(content) if content else "None"
        except Exception:
            summary = "N/A"
            content_hash = "error"
        return cls(
            path=path,
            sha256=content_hash,
            summary=summary,
        )

    async def refresh(self) -> "CodeBaseFile":
        try:
            content = self.path.read_text()
        except UnicodeDecodeError:
            content = "N/A"
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        if self.sha256 != content_hash:
            return await CodeBaseFile.from_path(self.path)
        return self

    def __str__(self, indent: int = 0) -> str:
        return (
            " " * indent
            + f"<file {self.path.name}>"
            + f": [green]{self.summary}[/green] </endfile {self.path.name}>"
        )


class CodeBaseTree(CodeBaseNode):
    nodes: list[Union["CodeBaseFile", "CodeBaseTree"]] = []

    def __init__(self, path: Path | str, **data: Any) -> None:
        data["name"] = Path(path).as_posix()
        super().__init__(**data)

    @classmethod
    def from_dict(cls, data: dict) -> "CodeBaseTree":
        path = data.pop("name")
        nodes_data = data.pop("nodes")
        nodes = [
            CodeBaseFile.from_dict(node_data)
            if "summary" in node_data
            else CodeBaseTree.from_dict(node_data)
            for node_data in nodes_data
        ]
        return cls(path, nodes=nodes, **data)

    @classmethod
    async def load(cls) -> "CodeBaseTree":
        if Path(".context/tree.yaml").exists():
            with open(".context/tree.yaml", "r") as f:
                data = yaml.safe_load(f)
                if not data:
                    return await cls.new()
                tree = cls.from_dict(data)
                return await tree.refresh()
        else:
            return await cls.new()

    @classmethod
    async def from_path(cls, path: Path) -> "CodeBaseTree":
        tasks = [
            CodeBaseFile.from_path(file_path)
            if file_path.is_file()
            else cls.from_path(file_path)
            for file_path in path.iterdir()
            if not is_ignored_by_gitignore(file_path.as_posix())
        ]
        if len(tasks) > 50:
            input(f"Found {len(tasks)} files in {path}. Press enter to continue...")
        nodes: list["CodeBaseNode"] = await asyncio.gather(*tasks)

        folder_hash = hashlib.sha256(
            ("".join(str(node.sha256) for node in nodes)).encode()
        ).hexdigest()

        tree = cls(
            path=path,
            sha256=folder_hash,
            nodes=nodes,
        )
        tree.to_yaml(".context/tree.yaml")
        return tree

    @classmethod
    async def new(cls) -> "CodeBaseTree":
        return await cls.from_path(Path("."))

    async def refresh(self) -> "CodeBaseTree":
        # gather new nodes from codebase not in self.nodes
        node_paths = [node.path for node in self.nodes]
        new_node_tasks = [
            CodeBaseFile.from_path(file_path)
            if file_path.is_file()
            else CodeBaseTree.from_path(file_path)
            for file_path in self.path.iterdir()
            if not is_ignored_by_gitignore(file_path.as_posix())
            and file_path not in node_paths
        ]
        # check node hash and update if necessary
        node_updates = [
            node
            for node in self.nodes
            if node.path
            in [
                file_path
                for file_path in self.path.iterdir()
                if not is_ignored_by_gitignore(file_path.as_posix())
            ]
        ]

        # delete nodes not in codebase anymore
        ignored_nodes = [
            file_path
            for file_path in self.path.iterdir()
            if not is_ignored_by_gitignore(file_path.as_posix())
        ]
        deleted_nodes = [node for node in self.nodes if node.path not in ignored_nodes]

        # update self.nodes
        self.nodes = [node for node in self.nodes if node not in deleted_nodes]
        self.nodes = [node for node in self.nodes if node not in node_updates]
        self.nodes.extend(
            await asyncio.gather(
                *new_node_tasks, *[node.refresh() for node in node_updates]
            )
        )

        # update self.sha256
        folder_hash = hashlib.sha256(
            ("".join(str(node.sha256) for node in self.nodes)).encode()
        ).hexdigest()

        if self.sha256 != folder_hash:
            self.sha256 = folder_hash
            self.to_yaml(".context/tree.yaml")

        return self

    @property
    def files(self) -> list[CodeBaseFile]:
        files = []
        for node in self.nodes:
            if isinstance(node, CodeBaseFile):
                files.append(node)
            else:
                files.extend(node.files)
        return files

    def __str__(self, indent: int = 0) -> str:
        folder_str = " " * indent + f"<folder {self.path.name}>\n"
        for node in self.nodes:
            folder_str += node.__str__(indent + 2) + "\n"
        folder_str += " " * indent + f"</endfolder {self.path.name}>\n"
        return folder_str

    def __repr__(self) -> str:
        return f"CodeBaseTree(path={self.path}, files={len(self.files)}, nodes={len(self.nodes)})"

    def show(self) -> str:
        return self.__str__()

    def to_yaml(self, file_path: Union[str, Path]) -> None:
        """
        Serialize the object to a YAML file.
        """
        # Ensure the directory exists before writing the file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w+") as f:
            yaml.safe_dump(self.dict(exclude_none=True), f)

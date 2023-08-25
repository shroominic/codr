import os
import yaml
import fnmatch
import asyncio
import hashlib
from typing import Union
from pathlib import Path
from pydantic import BaseModel


def is_ignored_by_gitignore(file_path: str, gitignore_path: str = ".gitignore") -> bool:
    """
    Checks if the given file path is ignored by the patterns in .gitignore or starts with a dot.
    """
    if os.path.basename(file_path).startswith("."):
        return True

    with open(gitignore_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        # Remove leading and trailing whitespaces and comments
        pattern = line.strip().split("#")[0]

        if pattern:
            if fnmatch.fnmatch(file_path, pattern) or fnmatch.fnmatch(os.path.basename(file_path), pattern):
                return True
    return False


class CodeBaseNode(BaseModel):
    name: str
    sha256: str
    embedding: list[float] | None = None

    @property
    def path(self) -> Path:
        return Path(".") / self.name

    @path.setter
    def path(self, value: Union[str, Path]):
        self.name = Path(value).relative_to(Path.cwd()).as_posix()

    def __str__(self, indent=0):
        return " " * indent + f"Node: {self.path.name}"


class CodeBaseFile(CodeBaseNode):
    summary: str

    def __init__(self, path: Path | str, **data):
        data["name"] = Path(path).as_posix()
        super().__init__(**data)

    @classmethod
    def from_dict(cls, data: dict) -> "CodeBaseFile":
        path = data.pop("name")
        return cls(path, **data)

    @classmethod
    async def from_path(cls, path: Path) -> "CodeBaseFile":
        from llm.chains import summarize_file

        content = path.read_text()
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        try:
            summary = await summarize_file(content)
        except Exception as e:
            print(f"Failed to summarize file {path}: {e.__class__.__name__}: {e.args[0]}")
            summary = "N/A"
        return cls(
            path=path,
            sha256=content_hash,
            summary=summary,
        )

    async def refresh(self) -> "CodeBaseFile":
        content = self.path.read_text()
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        if self.sha256 != content_hash:
            print("Old hash:", self.sha256, "New hash:", content_hash)
            return await CodeBaseFile.from_path(self.path)
        return self

    def __str__(self, indent=0):
        return " " * indent + f"<{self.path.name}" + f": {self.summary}>"


class CodeBaseTree(CodeBaseNode):
    nodes: list[Union["CodeBaseFile", "CodeBaseTree"]] = []

    def __init__(self, path: Path | str, **data):
        data["name"] = Path(path).as_posix()
        super().__init__(**data)

    @classmethod
    def from_dict(cls, data: dict) -> "CodeBaseTree":
        path = data.pop("name")
        nodes_data = data.pop("nodes")
        nodes = [
            CodeBaseFile.from_dict(node_data) if "summary" in node_data else CodeBaseTree.from_dict(node_data)
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
            CodeBaseFile.from_path(file_path) if file_path.is_file() else cls.from_path(file_path)
            for file_path in path.iterdir()
            if not is_ignored_by_gitignore(file_path.as_posix())
        ]
        nodes: list["CodeBaseNode"] = await asyncio.gather(*tasks)

        folder_hash = hashlib.sha256(("".join(str(node.sha256) for node in nodes)).encode()).hexdigest()

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
        folder_hash = hashlib.sha256(("".join(str(node.sha256) for node in self.nodes)).encode()).hexdigest()
        if self.sha256 != folder_hash:
            self.nodes = await asyncio.gather(*[node.refresh() for node in self.nodes])
        return self

    def __str__(self, indent=0):
        folder_str = " " * indent + f"<{self.path.name}>\n"
        for node in self.nodes:
            folder_str += node.__str__(indent + 2) + "\n"
        return folder_str

    def show(self) -> str:
        return self.__str__()

    def to_yaml(self, file_path: Union[str, Path]) -> None:
        """
        Serialize the object to a YAML file.
        """
        # Ensure the directory exists before writing the file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w+") as f:
            yaml.safe_dump(self.model_dump(exclude_none=True), f)

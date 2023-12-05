import asyncio
import hashlib
import yaml  # type: ignore
import os

from pathlib import Path
from typing import Any, Union, Coroutine

from .file import CodeBaseFile
from .node import CodeBaseNode
from .ignore import is_ignored_by_gitignore


class CodeBaseTree(CodeBaseNode):
    nodes: list[CodeBaseNode] = []

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
        tasks: list[Coroutine[Any, Any, CodeBaseNode]] = [
            CodeBaseFile.from_path(file_path)
            if file_path.is_file()
            else cls.from_path(file_path)
            for file_path in path.iterdir()
            if not is_ignored_by_gitignore(file_path.as_posix())
        ]
        if len(tasks) > 50:
            input(f"Found {len(tasks)} files in {path}. Press enter to continue...")
        nodes: list[CodeBaseNode] = await asyncio.gather(*tasks)

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

        if self.sha256 != folder_hash:  # type: ignore
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
                assert isinstance(node, CodeBaseTree)
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

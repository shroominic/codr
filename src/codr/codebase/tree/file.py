import hashlib
from pathlib import Path
from typing import Any

from .node import CodeBaseNode


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
        try:
            from ...llm.chains.files import summarize_file
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
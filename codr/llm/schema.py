from typing import Any, Union

from pydantic.v1 import BaseModel, Field


class Task(BaseModel):
    name: str
    description: str


class File(BaseModel):
    relative_path: str = Field(..., description="Relative File Path")


class PlannedFileChange(File):
    method: str = Field(..., description="StringEnum (create, modify, mkdir, delete)")
    description: str = Field(..., description="AbstractDescription (what to change)")

    @property
    def content(self) -> str:
        from ..codebase.func import read_file_sync

        return read_file_sync(self.relative_path)

    def __str__(self) -> str:
        icon = (
            "📄"
            if self.method == "create"
            else "📂"
            if self.method == "mkdir"
            else "📝"
            if self.method == "modify"
            else "🗑️"
            if self.method == "delete"
            else "❓"
        )
        return f"{icon} {self.relative_path} ({self.description})"


class PlannedFileChanges(BaseModel):
    changes: list[PlannedFileChange] = Field(..., description="List of file changes to make")

    def __iter__(self) -> Any:
        return iter(self.changes)

    def __str__(self) -> str:
        return "\n\n".join(str(change) for change in self.changes)


class CreatedFile(File):
    content: str = Field(..., description="New File Content")


class CreateDirectory(File):
    pass


class ModifiedFile(File):
    content: str = Field(..., description="New File Content")


class DeletedFile(File):
    pass


FileChange = Union[
    CreatedFile,
    CreateDirectory,
    ModifiedFile,
    DeletedFile,
]

from typing import Union
from pydantic import BaseModel, Field
from pathlib import Path


class Task(BaseModel):
    name: str
    description: str

    def __str__(self):
        return self.description


class File(BaseModel):
    relative_path: str = Field(..., description="Relative File Path")


class PlannedFileChange(File):
    method: str = Field(..., description="StringEnum (create, modify, delete)")
    description: str = Field(..., description="AbstractDescription (what to change)")

    @property
    def content(self):
        from codeio.codebase import CodeBase

        return CodeBase().read_file_str(Path(self.relative_path))


class PlannedFileChanges(BaseModel):
    changes: list[PlannedFileChange] = Field(..., description="List of file changes to make")

    def __iter__(self):
        return iter(self.changes)


class CreatedFile(File):
    content: str = Field(..., description="New File Content")


# class ModifiedFile(File):
#     changes: list[tuple[int, str, str]] = Field(..., description="List of changes to make")
class ModifiedFile(File):
    content: str = Field(..., description="New File Content")


class DeletedFile(File):
    pass


FileChange = Union[CreatedFile, ModifiedFile, DeletedFile]

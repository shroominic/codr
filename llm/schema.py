from typing import Union
from pydantic import BaseModel, Field


class Task(BaseModel):
    name: str
    description: str

    def __str__(self):
        return self.description


class File(BaseModel):
    path: str = Field(..., description="Relative File Path")


class PlannedFileChange(File):
    method: str = Field(..., description="StringEnum (create, modify, delete)")
    description: str = Field(..., description="AbstractDescription (what to change)")


class PlannedFileChanges(BaseModel):
    changes: list[PlannedFileChange] = Field(..., description="List of file changes to make")

    def __iter__(self):
        return iter(self.changes)


class CreatedFile(File):
    content: str = Field(..., description="New File Content")


class ModifiedFile(File):
    changes: list[tuple[int, str, str]] = Field(..., description="List of changes to make")


class DeletedFile(File):
    pass


FileChange = Union[CreatedFile, ModifiedFile, DeletedFile]

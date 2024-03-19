from typing import Any, Literal, Union

from pydantic import BaseModel, Field, field_validator


class Task(BaseModel):
    name: str | None = Field(default=None, description="Task Name")
    description: str


class File(BaseModel):
    relative_path: str = Field(description="Relative File Path, must start with ./ and exist in codebase")

    @field_validator("relative_path")
    @classmethod
    def validate_relative_path(cls, v: str) -> str:
        if not v.startswith("./"):
            raise ValueError("Relative Path must start with ./")
        # if not in_codebase(v):
        #     raise ValueError("File must exist in codebase")
        return v


class PlannedFileChange(File):
    method: Literal["create", "modify", "mkdir", "delete"] = Field(description="Method enum of action to apply.")
    description: str = Field(description="AbstractDescription (plan on what to change) make sure to be extra precise.")

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
    changes: list[PlannedFileChange] = Field(description="List of file changes to make")

    def __iter__(self) -> Any:
        return iter(self.changes)

    def __str__(self) -> str:
        return "\n\n".join(str(change) for change in self.changes)


class CreatedFile(File):
    content: str = Field(description="New File Content")


class CreateDirectory(File):
    pass


def diff(content: str, relative_path: str) -> str:
    from ..codebase.func import read_file_sync

    old_content = read_file_sync(relative_path)
    from difflib import unified_diff

    return "\n".join(unified_diff(old_content.splitlines(), content.splitlines()))


class ModifiedFile(File):
    content: str = Field(description="New File Content")

    def print_diff(self) -> None:
        for line in diff(
            self.content,
            self.relative_path,
        ).splitlines():
            if line.startswith("+"):
                print(f"\033[92m{line}\033[0m")
            elif line.startswith("-"):
                print(f"\033[91m{line}\033[0m")
            else:
                print(f"{line}")


class DeletedFile(File):
    pass


FileChange = Union[
    CreatedFile,
    CreateDirectory,
    ModifiedFile,
    DeletedFile,
]

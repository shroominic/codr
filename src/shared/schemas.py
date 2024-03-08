from typing import Literal

from pydantic import BaseModel, Field

Data = str | bytes


class WSMessage(BaseModel):
    type: Literal["msg", "error", "action", "codebaseio"] = Field(..., description="Type of the object.")
    data: BaseModel | str = Field(..., description="Data of the object.")
    action: str | None = Field(None, description="Action class name.")


class Message(BaseModel):
    content: str


class Error(Message):
    log: str | None


class ResultModel(BaseModel):
    status: Literal["healthy", "error"] = "healthy"


class ActionResult(ResultModel): ...


class CodeBaseIOResult(ResultModel):
    data: Data | None = None
    path: str | None = None

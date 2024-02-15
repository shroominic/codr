from hashlib import sha256

from pydantic import BaseModel

from .codebase import CodeBase


class Session(BaseModel):
    api_key_hash: str

    def __init__(
        self,
        openai_api_key: str,
    ) -> None:
        self.openai_api_key = openai_api_key
        self.api_key_hash = sha256(openai_api_key.encode()).hexdigest()
        self.codebase = CodeBase(self)

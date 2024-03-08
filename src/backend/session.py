from hashlib import sha256
from typing import Any

from pydantic import BaseModel


class Session(BaseModel):
    api_key_hash: str

    def __init__(
        self,
        openai_api_key: str,
        **data: Any,
    ) -> None:
        data["api_key_hash"] = sha256(openai_api_key.encode()).hexdigest()
        super().__init__(**data)
        self.openai_api_key = openai_api_key

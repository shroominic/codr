from funcchain import settings

from .cli import app

settings.llm = "gpt-4-1106-preview"


if __name__ == "__main__":
    app()

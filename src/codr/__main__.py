from funcchain import settings
from .cli import app

settings.MODEL_NAME = "gpt-4-1106-preview"


if __name__ == "__main__":
    app()

from funcchain import settings

settings.llm = "gpt-4-turbo-preview"


if __name__ == "__main__":
    from .cli import app

    app()

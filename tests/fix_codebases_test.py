import asyncio
import os

from utils import shell


async def prepare_environments(example: str) -> None:
    await shell("uv venv", cwd="tests/codebases/playgrounds/" + example)

    if "requirements.txt" in os.listdir(f"tests/codebases/playgrounds/{example}"):
        print(f"Installing requirements for {example} ...")
        await shell("uv pip install -r requirements.txt", cwd="tests/codebases/playgrounds/" + example)


async def run_debugging(example: str) -> None:
    await shell(
        "codr debug '.venv/bin/python main.py'",
        cwd="tests/codebases/playgrounds/" + example,
        ignore_stdout=False,
    )


async def reset_environments() -> None:
    await shell("rm -rf playgrounds", cwd="tests/codebases/", ignore_stdout=False)


async def fix_codebases() -> None:
    await shell("cp -r tests/codebases/examples/ tests/codebases/playgrounds/")

    fix_examples = [
        example
        for example in os.listdir("tests/codebases/examples")
        if os.path.isdir("tests/codebases/examples/" + example) and example.startswith("fix_")
    ]
    try:
        # todo optimize async
        for example in fix_examples:
            print("Fixing", example)
            await prepare_environments(example)
            print("Running debugging for", example)
            await run_debugging(example)

    finally:
        await reset_environments()


def test_fix_codebases() -> None:
    asyncio.run(fix_codebases())


if __name__ == "__main__":
    test_fix_codebases()

import asyncio
import os
from asyncio import subprocess


async def prepare_environments(example_path: str) -> None:
    await subprocess.create_subprocess_shell(
        "python3 -m venv venv && source venv/bin/activate &&pip install -r requirements.txt",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="playgrounds/" + example_path,
    )


async def run_debugging(example_path: str) -> None:
    await subprocess.create_subprocess_shell(
        "conda activate neural-cli && codr debug 'venv/bin/python3 main.py'",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="playgrounds/" + example_path,
    )


async def fix_codebases() -> None:
    # copy example codebases to new created playgrounds
    os.system("cp -r examples/ playgrounds/")

    fix_examples = [
        example for example in os.listdir("examples") if os.path.isdir(example) and example.startswith("fix_")
    ]

    await asyncio.gather(prepare_environments(example_path) for example_path in fix_examples)


def test_fix_codebases() -> None:
    assert True


if __name__ == "__main__":
    test_fix_codebases()

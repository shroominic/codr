import asyncio
import os
from asyncio import subprocess as asp


async def prepare_environments(example_path: str) -> None:
    await asp.create_subprocess_shell(
        # todo optimize with uv
        "python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt",
        cwd="tests/codebases/playgrounds/" + example_path,
    )


async def run_debugging(example_path: str) -> None:
    await asp.create_subprocess_shell(
        "codr debug '.venv/bin/python3 main.py'",
        stdout=asp.PIPE,
        stderr=asp.PIPE,
        cwd="tests/codebases/playgrounds/" + example_path,
    )


async def reset_environments(example_path: str) -> None:
    await asp.create_subprocess_shell("rm -rf playgrounds", cwd="tests/codebases/")


async def fix_codebases() -> None:
    # copy example codebases to new created playgrounds
    os.system("cp -r examples/ playgrounds/")

    fix_examples = [
        example for example in os.listdir("examples") if os.path.isdir(example) and example.startswith("fix_")
    ]

    await asyncio.gather(prepare_environments(example_path) for example_path in fix_examples)


def test_fix_codebases() -> None:
    asyncio.run(fix_codebases())


if __name__ == "__main__":
    test_fix_codebases()

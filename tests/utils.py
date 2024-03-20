from asyncio import subprocess
from typing import Optional


async def shell(command: str, cwd: Optional[str] = None, ignore_stdout: bool = True) -> None:
    extra_args: dict = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE} if ignore_stdout else {}
    if cwd:
        extra_args["cwd"] = cwd

    try:
        p = await subprocess.create_subprocess_shell(command, **extra_args)
        await p.wait()

    except Exception as e:
        print(f"Error: {e}")

        if "p" in locals():
            p.terminate()
            await p.wait()

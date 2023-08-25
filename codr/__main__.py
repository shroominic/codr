import asyncio
import typer

from codr.llm.scripts import solve_task
from codr.llm.schema import Task
from codr.llm.chains import summarize_task_to_name, check_result, generate_task
from codr.codebase import CodeBase

app = typer.Typer()


@app.command()
def solve(task_description: str):
    task_name = summarize_task_to_name(task_description)
    print("Task name:", task_name)
    task = Task(
        name=task_name,
        description=task_description,
    )
    asyncio.run(solve_task(task))
    debug()


@app.command()
def debug():
    result = CodeBase().bash_str_sync("./test.sh")

    print("RESULT: ", result)

    if check_result(result):
        return print("DEBUG SUCCESSFUL")
    
    task = generate_task(result)
    print("TASK:", task)
    solve(task)


@app.command()
def test():
    
    print("test successful")


if __name__ == "__main__":
    app()

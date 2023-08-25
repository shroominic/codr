import asyncio
import typer

# from codr.llm.chains import ask_additional_question
from codr.llm.scripts import solve_task
from codr.llm.schema import Task
from codr.llm.chains import summarize_task_to_name, check_result, gather_run_cmd, generate_task
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


@app.command()
def debug():
    codebase = CodeBase()
    tree = codebase.get_tree_sync()
    
    cmd = gather_run_cmd(tree).code
    
    result = codebase.bash_str_sync(cmd)

    if not check_result(result):
        task = generate_task(result)
        solve(task)

            
    


if __name__ == "__main__":
    app()

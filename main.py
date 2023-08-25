import asyncio
import typer

# from llm.chains import ask_additional_question
from llm.scripts import solve_task
from llm.schema import Task
from llm.chains import summarize_task_to_name


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


# @app.command()
# def debug():
#     instructions = gather_run_instructions(codebase)
#     result = codebase.run(instructions)

#     if not check_result(result):
#         task = generate_task(result)
#         solution = solve(task)
#         if solution:
#             print("Solution:", solution)
#         else:
#             debug()


if __name__ == "__main__":
    app()

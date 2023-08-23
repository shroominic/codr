import asyncio
import typer
# from llm.chains import ask_additional_question
from llm.scripts import solve_task
from llm.schema import Task


app = typer.Typer()


@app.command()
def solve():
    task = Task(
        # TODO: auto create name from description
        name=typer.prompt("Task name: "),
        description=typer.prompt("Task description: "),
    )
    # extra_info = (q := ask_additional_question(task)) and typer.prompt(q)

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

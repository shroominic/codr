from InquirerPy import inquirer
from InquirerPy.base.control import Choice


async def show_yes_no_select(
    question: str,
) -> bool:
    """
    Show cli select for yes or no
    """
    return (
        await inquirer.select(  # type: ignore
            message=question,
            choices=[
                Choice("y", "yes"),
                Choice("n", "no"),
            ],
        ).execute_async()
        == "y"
    )


if __name__ == "__main__":
    print(show_yes_no_select("Do you want to continue?"))

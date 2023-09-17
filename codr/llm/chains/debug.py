from funcchain.chain import achain


async def check_result(result: str) -> bool:
    """
    CONSOLE OUTPUT:
    {result}

    Is the output healthy? Answer with "yes" or "no".
    """
    return await achain()


async def check_desired_output(result: str, goal: str) -> bool:
    """
    CONSOLE OUTPUT:
    {result}

    DESIRED OUTPUT (DESCRIPTION):
    {goal}

    Is the output what is desired? Answer with "yes" or "no".
    """
    return await achain()

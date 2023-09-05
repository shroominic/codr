from funcchain.shortcuts import afuncchain


async def check_result(result: str) -> bool:
    """
    CONSOLE OUTPUT:
    {result}

    Is the output healthy? Answer with "yes" or "no".
    """
    return await afuncchain()

from funcchain import achain


async def check_result(console_output: str) -> bool:
    """
    Is the output healthy? Answer with "yes" or "no".
    """
    return await achain()


async def check_desired_output(
    console_output: str,
    desired_output_description: str,
) -> bool:
    """
    Is the output what is desired? Answer with "yes" or "no".
    """
    return await achain()

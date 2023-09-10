import pytest
from funcchain.shortcuts import afuncchain


async def check_result(result: str) -> bool:
    """
    CONSOLE OUTPUT:
    {result}

    Is the output healthy? Answer with "yes" or "no".
    """
    return await afuncchain()


async def check_desired_output(result: str, goal: str) -> bool:
    """
    CONSOLE OUTPUT:
    {result}

    DESIRED OUTPUT (DESCRIPTION):
    {goal}

    Is the output what is desired? Answer with "yes" or "no".
    """
    return await afuncchain()


# Test cases for check_result function
@pytest.mark.asyncio
async def test_check_result():
    assert await check_result("Healthy output") == True
    assert await check_result("Unhealthy output") == False


# Test cases for check_desired_output function
@pytest.mark.asyncio
async def test_check_desired_output():
    assert await check_desired_output("Desired output", "Desired output") == True
    assert await check_desired_output("Undesired output", "Desired output") == False

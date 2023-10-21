from langchain.memory import ChatMessageHistory

# from codr.llm.scripts import auto_debug, commit_changes, expert_answer, solve_task

HISTORY = ChatMessageHistory()


async def chat(user_query: str) -> str:
    """
    Get a response from the chat agent.
    """
    # route to the query to the chat agent

    # ROUTER = Union[Tools...]

    # route = await select_route(user_query)  # type: ignore

    return ""  # await route()

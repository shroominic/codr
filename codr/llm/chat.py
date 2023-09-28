from langchain.memory import ChatMessageHistory
from codr.llm.scripts import solve_task, auto_debug, commit_changes, expert_answer

HISTORY = ChatMessageHistory()

async def chat(user_query: str) -> str:
    """
    Get a response from the chat agent.
    """
    # route to the query to the chat agent
    
    ROUTER = Union[Tools...]
    
    route = await select_route(user_query)
    
    return await route()

from funcchain import achain
from langchain.pydantic_v1 import BaseModel, Field


class QueryHandler(BaseModel):
    query_name: str = Field(..., description="Selected query handler.")



async def select_query_handler(user_query: str, query_handlers: dict) -> QueryHandler:
    """
    USER QUERY:
    {user_query}

    QUERY HANDLERS:
    {query_handlers}

    Select a query handler that fits best for the user query.
    """
    return await achain()


if __name__ == "__main__":
    import asyncio
    
    # Define a dictionary of query handlers. Each key is a command that the user can input,
    # and the corresponding value is a description of what that command does.
    query_handlers = {
        "implement": "Implement a feature to the codebase.",
        "fix": "Fix a bug in the codebase.",
        "test": "Test the codebase.",
        "debug": "Debug the codebase.",
        "refactor": "Refactor the codebase.",
        "review": "Review the codebase.",
        "document": "Document the codebase.",
        "ask": "Ask a question about the codebase.",
        "commit": "Commit current changes.",
        "tree": "Print the current tree.",
        "other": "Do something else.",
        "config": "Configure the chat app (change api-key, other settings)."
    }
    
    # Define a user query. This is the command that the user wants to execute.
    user_query = "Fix this bug"
    
    # Run the select_query_handler function asynchronously. This function will select the
    # appropriate query handler based on the user's query.
    query_handler = asyncio.run(
        select_query_handler(user_query, query_handlers)
    )
    
    # Print the selected query handler.
    print(query_handler)

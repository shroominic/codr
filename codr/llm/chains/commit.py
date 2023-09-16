from funcchain.parser import LambdaOutputParser
from funcchain.chain import achain, chain
from funcchain.utils import raiser
from emoji import is_emoji


async def write_commit_message(file_name: str, modifications: str) -> str:
    """
    FILE:
    {file_name}

    MODIFICATIONS:
    {modifications}

    Write a tiny commit message for these file changes.
    Start with a emoji and never answer with more than 5 words.
    Example: 🐛 Fix bug in foo.py
    """
    return await achain(
        # parser=LambdaOutputParser(
        #     _parse=(lambda t: t if len(t.split()) > 6 else summarize_commit_message(t)),
        # )
    )


def summarize_commit_message(msg: str) -> str:
    """
    COMMIT MESSAGE:
    {msg}

    Summarize commit message. Answer with a compressed piece of knowledge.
    Start with a emoji and answer with less than 6 words.
    """
    return chain(
        parser=LambdaOutputParser(
            _parse=lambda t: t if is_emoji(t.split()[0]) else raiser(ValueError("Start with an emoji.")),
        )
    )

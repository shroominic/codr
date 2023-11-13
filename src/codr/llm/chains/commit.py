from funcchain import achain
from funcchain.parser import LambdaOutputParser
from funcchain.utils import raiser


async def write_commit_message(file_name: str, modifications: str) -> str:
    """
    Write a tiny commit message for these file changes.
    Start with a emoji and never answer with more than 5 words.
    Example: 🐛 Fix bug in foo.py
    """
    return await achain()


async def summarize_commit_message(commit_message: str) -> str:
    """
    Summarize commit message. Answer with a compressed piece of knowledge.
    Start with a emoji and answer with less than 6 words.
    """
    from emoji import is_emoji

    return await achain(
        parser=LambdaOutputParser(
            _parse=lambda t: t
            if is_emoji(t.split()[0])
            else raiser(ValueError("Start with an emoji.")),
        )
    )

import asyncio
import inspect
from os import getenv
from dotenv import load_dotenv

from typing import TypeVar
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI, AzureChatOpenAI
from langchain.chat_models.base import BaseChatModel
from langchain.output_parsers import BooleanOutputParser, PydanticOutputParser, CommaSeparatedListOutputParser
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import (
    BaseMessage,
    SystemMessage,
    BaseOutputParser,
    StrOutputParser,
)

from llm.templates import solve_task_system_instruction
from funcchain.utils import count_tokens, retry
from funcchain.parser import CodeBlock, ParserBaseModel


load_dotenv()

T = TypeVar("T")


def _get_llm(model: str) -> BaseChatModel:
    verbose = getenv("VERBOSE", "false").lower() == "true"
    if "azure" in model:
        return AzureChatOpenAI(
            model="gpt-4-32k",
            deployment_name="giga-4",
            openai_api_key=getenv("AZURE_OPENAI_API_KEY", ""),
            openai_api_base="https://science.openai.azure.com/",
            openai_api_type="azure",
            openai_api_version="2023-07-01-preview",
            verbose=verbose,
        )
    if "gpt" in model:
        print("Using: ", model)
        return ChatOpenAI(
            model=model,
            verbose=verbose,
            request_timeout=60 * 5,
            openai_api_key=getenv("OPENAI_API_KEY", ""),
        )
    raise ValueError(f"Unknown model: {model}")


def _from_docstring() -> str:
    """
    Get the docstring of the parent caller function.
    """
    return (
        (caller_frame := inspect.getouterframes(inspect.currentframe())[3])
        .frame.f_globals[caller_frame.function]
        .__doc__
    )


def _parser_from_type() -> BaseOutputParser:
    """
    Get the parser from the type annotation of the parent caller function.
    """
    output_type = (
        (caller_frame := inspect.getouterframes(inspect.currentframe())[3])
        .frame.f_globals[caller_frame.function]
        .__annotations__["return"]
    )
    if output_type is str:
        return StrOutputParser()
    if output_type is bool:
        return BooleanOutputParser()
    if issubclass(output_type, ParserBaseModel):
        return output_type.output_parser()
    if issubclass(output_type, BaseModel):
        return PydanticOutputParser(pydantic_object=output_type)
    else:
        raise NotImplementedError(f"Unknown output type: {output_type}")


def _kwargs_from_parent() -> dict[str, str]:
    """
    Get the kwargs from the parent function.
    """
    return inspect.getouterframes(inspect.currentframe())[3].frame.f_locals


@retry(3)
def funcchain(
    instruction: HumanMessagePromptTemplate | str | None = None,
    system: SystemMessage | SystemMessagePromptTemplate = solve_task_system_instruction,
    parser: BaseOutputParser[T] | None = None,
    context: list[BaseMessage] = [],
    model: str = "gpt-4",
    max_tokens: int = 8192 - 2048,
    /,
    **input_kwargs,
) -> T:
    """
    Get response from chatgpt for provided instructions.
    """
    if not instruction:
        instruction = _from_docstring()
    if not input_kwargs:
        input_kwargs = _kwargs_from_parent()
    if not parser:
        parser = _parser_from_type()

    base_tokens = count_tokens(
        instruction
        if isinstance(instruction, str)
        else str(instruction.prompt) + str(system.prompt)
        if isinstance(system, SystemMessagePromptTemplate)
        else system.content
    )
    print("BaseTokens: ", base_tokens)

    for k, v in input_kwargs.copy().items():
        if isinstance(v, str):
            content_tokens = count_tokens(v)
            print("ContentTokens: ", content_tokens)
            if base_tokens + content_tokens > max_tokens:
                input_kwargs[k] = v[: (max_tokens - base_tokens) * 2 // 3]
                print("Truncated: ", len(input_kwargs[k]))

    print("InputKwargs: ", input_kwargs)

    prompt = ChatPromptTemplate.from_messages(
        [system]
        + context
        + [
            HumanMessagePromptTemplate.from_template(template=instruction)
            if isinstance(instruction, str)
            else instruction
        ]
    )
    return (prompt | _get_llm(model=model) | parser).invoke(input_kwargs)


@retry(3)
async def afuncchain(
    instruction: HumanMessagePromptTemplate | str | None = None,
    system: SystemMessage | SystemMessagePromptTemplate = solve_task_system_instruction,
    parser: BaseOutputParser[T] | None = None,
    context: list[BaseMessage] = [],
    model: str = "gpt-4",
    max_tokens: int = 8192 - 2048,
    /,
    **input_kwargs,
) -> T:
    """
    Get response from chatgpt for provided instructions.
    """
    if not instruction:
        instruction = _from_docstring()
    if not input_kwargs:
        input_kwargs = _kwargs_from_parent()
    if not parser:
        parser = _parser_from_type()

    base_tokens = count_tokens(
        instruction
        if isinstance(instruction, str)
        else str(instruction.prompt) + str(system.prompt)
        if isinstance(system, SystemMessagePromptTemplate)
        else system.content
    )
    print("BaseTokens: ", base_tokens)

    for k, v in input_kwargs.copy().items():
        if isinstance(v, str):
            content_tokens = count_tokens(v)
            print("ContentTokens: ", content_tokens)
            if base_tokens + content_tokens > max_tokens:
                input_kwargs[k] = v[: (max_tokens - base_tokens) * 2 // 3]
                print("Truncated: ", len(input_kwargs[k]))

    print("InputKwargs: ", input_kwargs)

    prompt = ChatPromptTemplate.from_messages(
        [system]
        + context
        + [
            HumanMessagePromptTemplate.from_template(template=instruction)
            if isinstance(instruction, str)
            else instruction
        ]
    )
    return await (prompt | _get_llm(model=model) | parser).ainvoke(input_kwargs)

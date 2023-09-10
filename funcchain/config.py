"""
Funcchain Settings:
Automatically loads environment variables from .env file
"""
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv("./.env")


class FuncchainSettings(BaseSettings):
    # General
    VERBOSE: bool = True

    # Prompt
    MAX_TOKENS: int = 32768 - 8192
    DEFAULT_SYSTEM_PROMPT: str = "You are an advanced programming assistant solving tasks for developers."

    # Model
    OPENAI_API_KEY: str = ""
    AZURE_API_KEY: str = ""
    AZURE_API_BASE: str = ""
    AZURE_DEPLOYMENT_NAME: str = ""
    AZURE_DEPLOYMENT_NAME_LONG: str = ""
    AZURE_API_VERSION: str = ""


settings = FuncchainSettings()

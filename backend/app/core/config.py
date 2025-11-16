"""
    Harkonnen Backend Config
"""

from typing import List

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application
    APP_NAME: str
    VERSION: str

    # Prefix
    API_PREFIX: str

    # Server
    HOST: str
    PORT: int
    
    # CORS - Chrome Extension Support
    ALLOWED_ORIGINS: List[str]


settings = Settings()

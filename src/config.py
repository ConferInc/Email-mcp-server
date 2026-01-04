from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

# Resolve path to .env file relative to this script
# src/config.py -> parent is src/ -> parent.parent is project root
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / '.env'

class EmailConfig(BaseSettings):
    """
    Configuration settings for the Email MCP Server.
    Reads from environment variables or .env file.
    """
    model_config = SettingsConfigDict(env_file=str(ENV_FILE), env_file_encoding='utf-8', extra='ignore')

    # SMTP (Sending)
    SMTP_HOST: str
    SMTP_PORT: int = 465  # Default to SSL port

    # IMAP (Receiving)
    IMAP_HOST: str
    IMAP_PORT: int = 993  # Default to SSL port

    # Credentials
    EMAIL_USER: str
    EMAIL_PASS: str

    @property
    def check_connection_enabled(self) -> bool:
        """Helper to check if minimal config is present"""
        return all([self.SMTP_HOST, self.IMAP_HOST, self.EMAIL_USER, self.EMAIL_PASS])

# Instantiate config
try:
    config = EmailConfig()
except Exception as e:
    print(f"Warning: Configuration loading failed: {e}")
    raise

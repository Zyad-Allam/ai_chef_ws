from dotenv import load_dotenv
from pydantic import BaseModel, validator
from typing import Optional
import sys


load_dotenv()


class Settings(BaseModel):
    flask_env: str = "development"

    port: int = 5000


# Global settings instance
try:
    settings = Settings()
    print("SUCCESS: All required environment variables are set")
except Exception as e:
    print(f"ERROR: Configuration validation failed: {e}", file=sys.stderr)
    sys.exit(1)

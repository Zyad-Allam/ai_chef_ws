import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logging():
    """Configure logging for the AI Teacher application"""

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(
                log_dir / f"ai_teacher_{datetime.now().strftime('%Y%m%d')}.log"
            ),
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Suppress noisy library loggers
    logging.getLogger("elasticsearch").setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.ERROR)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("azure").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("werkzeug").setLevel(logging.WARNING)  # Flask server logs

    # Application logger
    logger = logging.getLogger("ai_teacher")
    logger.setLevel(logging.INFO)

    return logger


# Initialize logging when module is imported
logger = setup_logging()

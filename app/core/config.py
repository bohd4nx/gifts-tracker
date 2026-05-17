import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Config:
    def __init__(self) -> None:
        env_path = Path(__file__).resolve().parents[2] / ".env"

        if env_path.exists():
            load_dotenv(env_path)
        elif not os.getenv("API_ID"):
            # no .env file and no env vars injected (e.g. via docker-compose env_file)
            logger.error("Configuration file not found! Please create '.env'")
            sys.exit(1)

        self.API_ID: int = int(os.getenv("API_ID", "0"))
        self.API_HASH: str = os.getenv("API_HASH", "")
        self.PHONE_NUMBER: str = os.getenv("PHONE_NUMBER", "")
        self.PASSWORD: str | None = os.getenv("PASSWORD") or None

        self.BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

        self.CHANNEL_ID: int = int(os.getenv("CHANNEL_ID", "0"))
        self.STICKERS_CHANNEL_ID: int = int(os.getenv("STICKERS_CHANNEL_ID", "0"))
        self.STICKERS_CHANNEL_USERNAME: str = os.getenv("STICKERS_CHANNEL_USERNAME", "")

        self.INTERVAL: float = float(os.getenv("INTERVAL", "15.0"))

        self.EMOJI_PACK_SHORT_NAME: str = os.getenv("EMOJI_PACK_SHORT_NAME", "GiftsTrackerPack")
        self.EMOJI_PACK_TITLE: str = os.getenv("EMOJI_PACK_TITLE", "Gifts by @GiftsTracker")

        self.DATABASE_URL: str = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://giftsuser:giftspass@localhost:5432/giftsdb",
        )


config = Config()

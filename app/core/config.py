import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Config:
    def __init__(self) -> None:
        env_path = Path(__file__).resolve().parents[2] / ".env"

        # Load .env when present; in Docker env vars are injected directly
        if env_path.exists():
            load_dotenv(env_path)

        self.DATABASE_URL: str = self._require("DATABASE_URL")

        self.API_ID: int = int(os.getenv("API_ID") or 2040)
        self.API_HASH: str = os.getenv("API_HASH") or "b18441a1ff607e10a989891a5462e627"
        self.PHONE_NUMBER: str = self._require("PHONE_NUMBER")
        self.PASSWORD: str | None = os.getenv("PASSWORD") or None

        self.BOT_TOKEN: str = self._require("BOT_TOKEN")

        self.CHANNEL_ID: int = int(self._require("CHANNEL_ID"))
        self.STICKERS_CHANNEL_ID: int = int(self._require("STICKERS_CHANNEL_ID"))
        self.STICKERS_CHANNEL_USERNAME: str = self._require("STICKERS_CHANNEL_USERNAME")

        self.EMOJI_PACK_SHORT_NAME: str = self._require("EMOJI_PACK_SHORT_NAME")
        self.EMOJI_PACK_TITLE: str = self._require("EMOJI_PACK_TITLE")

        self.INTERVAL: float = float(os.getenv("INTERVAL") or 15.0)

    @staticmethod
    def _require(name: str) -> str:
        value = os.getenv(name, "").strip()
        if not value:
            logger.error("Missing required environment variable: %s", name)
            sys.exit(1)
        return value


config = Config()

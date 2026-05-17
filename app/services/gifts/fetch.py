import logging
from dataclasses import asdict
from typing import Any

from pyrogram import Client, raw

from app.utils import parse_gift

logger = logging.getLogger(__name__)


async def fetch_gifts(app: Client, last_hash: int = 0) -> tuple[int, dict[int, dict[str, Any]] | None]:
    """Returns (new_hash, gifts_dict) or (last_hash, None) when the list is unchanged."""
    try:
        result = await app.invoke(raw.functions.payments.GetStarGifts(hash=last_hash))

        if isinstance(result, raw.types.payments.StarGiftsNotModified):
            logger.debug("Gift list unchanged since last check")
            return last_hash, None

        gifts = {gift.id: asdict(parse_gift(gift)) for gift in result.gifts}
        return result.hash, gifts or None
    except Exception:
        logger.exception("Failed to fetch gifts from Telegram API")
        return last_hash, None

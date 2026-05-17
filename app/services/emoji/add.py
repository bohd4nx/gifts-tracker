import asyncio
import logging
from typing import Any

from pyrogram import Client
from pyrogram.errors import FloodWait

from . import state
from .sticker_set import add_sticker_to_set, make_sticker_item

logger = logging.getLogger(__name__)


async def add_gift_to_pack(app: Client, gift: dict[str, Any]) -> int | None:
    if state.pack_ref is None or not gift.get("sticker_raw"):
        return None

    try:
        result = await add_sticker_to_set(app, state.pack_ref, make_sticker_item(gift["sticker_raw"]))
        emoji_id = result.documents[-1].id
        await asyncio.sleep(1.5)
        return emoji_id
    except FloodWait as e:
        logger.warning("FloodWait %ds — skipped adding gift %s to emoji pack", e.value, gift["id"])
        await asyncio.sleep(e.value)
        return None
    except Exception:
        logger.exception("Failed to add gift %s to emoji pack", gift["id"])
        return None

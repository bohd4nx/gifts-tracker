import asyncio
import logging
from typing import Any

from aiogram import Bot
from pyrogram import Client

from app.services.emoji import add_gift_to_pack

from .notification import notify_new_gift
from .upload import upload_gift_sticker

logger = logging.getLogger(__name__)


async def process_new_gifts(
    app: Client, bot: Bot, new_gifts: dict[int, dict[str, Any]], gifts_history: dict[int, dict[str, Any]]
) -> None:
    gifts = list(new_gifts.values())

    for idx, gift in enumerate(gifts, 1):
        logger.info("New gift %d/%d — id=%s", idx, len(gifts), gift["id"])

        try:
            sticker_msg_id, emoji_id = await asyncio.gather(
                upload_gift_sticker(app, bot, gift),
                add_gift_to_pack(app, gift),
            )

            if not sticker_msg_id:
                raise ValueError(f"Sticker upload returned None for gift {gift['id']}")

            gift["emoji_id"] = emoji_id
            gift["sticker_msg_id"] = sticker_msg_id

            # give Telegram time to index the sticker post before the link preview is built
            await asyncio.sleep(3)

            gift["msg_id"] = await notify_new_gift(app, gift, sticker_msg_id)
            gift["upgrade_msg_id"] = None

            logger.info("Gift %s processed successfully", gift["id"])
        except Exception:
            logger.exception("Failed to process gift %s", gift["id"])
            gift.update(sticker_msg_id=None, msg_id=None, upgrade_msg_id=None, emoji_id=None)

        gifts_history[gift["id"]] = gift

        if idx < len(gifts):
            await asyncio.sleep(1)

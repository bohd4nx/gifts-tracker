import logging
from io import BytesIO
from typing import Any

from aiogram import Bot
from aiogram.types import BufferedInputFile

from app.core import config

logger = logging.getLogger(__name__)


async def upload_gift_sticker(app: Any, bot: Bot, gift: dict[str, Any]) -> int | None:
    sticker_file_id = gift.get("sticker_file_id")
    if not sticker_file_id:
        logger.error("Missing sticker_file_id for gift %s", gift["id"])
        return None

    try:
        sticker_bytes: BytesIO = await app.download_media(sticker_file_id, in_memory=True)

        # TODO: fix cases when Telegram returns an empty or unrecognized file.
        # sometimes the downloaded media is not sent as a sticker by Telegram
        # (e.g. empty buffer or invalid format for .tgs).
        if not sticker_bytes or sticker_bytes.getbuffer().nbytes == 0:
            logger.error("Downloaded file is empty for gift %s", gift["id"])
            return None

        sticker = BufferedInputFile(file=sticker_bytes.getvalue(), filename="AnimatedSticker.tgs")
        message = await bot.send_sticker(chat_id=config.STICKERS_CHANNEL_ID, sticker=sticker)
        return message.message_id
    except Exception as e:
        logger.error("Upload error for gift %s: %s", gift["id"], e)
        return None

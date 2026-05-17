import asyncio
import logging

from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import LinkPreviewOptions

from app.core import config

logger = logging.getLogger(__name__)


async def send_msg(
    app: Client,
    text: str,
    link_preview: LinkPreviewOptions | None = None,
) -> int | None:
    try:
        msg = await app.send_message(
            chat_id=config.CHANNEL_ID,
            text=text,
            link_preview_options=link_preview,  # type: ignore[arg-type]
        )
        return msg.id
    except FloodWait as e:
        logger.warning("FloodWait %ds on send_msg, retrying...", e.value)
        await asyncio.sleep(e.value)
        return await send_msg(app, text, link_preview)
    except Exception:
        logger.exception("Failded to send message to channel")
        return None


async def edit_msg(
    app: Client,
    message_id: int,
    text: str,
    link_preview: LinkPreviewOptions | None = None,
) -> bool:
    try:
        await app.edit_message_text(
            chat_id=config.CHANNEL_ID,
            message_id=message_id,
            text=text,
            link_preview_options=link_preview,  # type: ignore[arg-type]
        )
        return True
    except FloodWait as e:
        logger.warning("FloodWait %ds on edit message_id=%d, retrying...", e.value, message_id)
        await asyncio.sleep(e.value)
        return await edit_msg(app, message_id, text, link_preview)
    except Exception:
        logger.exception("Failed to edit message_id=%d", message_id)
        return False

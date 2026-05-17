import logging
from typing import Any

from pyrogram import Client

from app.services.notifications.base import send_msg
from app.services.notifications.gifts import compose_text
from app.utils.display import create_link_preview, get_released_peer

logger = logging.getLogger(__name__)


async def notify_new_gift(app: Client, gift: dict[str, Any], sticker_msg_id: int) -> int | None:
    try:
        username = await get_released_peer(app, gift)
        text = compose_text(gift, username)
        link_preview = create_link_preview(gift, sticker_msg_id)
        return await send_msg(app, text, link_preview)
    except Exception:
        logger.exception("Failed to send notification for gift %s", gift.get("id"))
        return None

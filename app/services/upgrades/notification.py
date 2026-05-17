import logging
from typing import Any

from pyrogram import Client

from app.services.notifications.base import edit_msg, send_msg
from app.services.notifications.upgrades import compose_text
from app.utils.gifts import create_link_preview, get_released_peer

logger = logging.getLogger(__name__)


async def notify_upgrade_available(app: Client, gift: dict[str, Any]) -> None:
    sticker_msg_id = gift.get("sticker_msg_id")
    if not sticker_msg_id:
        return
    try:
        username = await get_released_peer(app, gift)
        text = compose_text(gift, username)
        link_preview = create_link_preview(gift, sticker_msg_id)
        msg_id = await send_msg(app, text, link_preview)
        gift["upgrade_msg_id"] = msg_id
        logger.info("Upgrade notification sent for gift %s, msg_id=%s", gift["id"], msg_id)
    except Exception:
        logger.exception("Failed to send upgrade notification for gift %s", gift.get("id"))


async def notify_upgrade_price_changed(app: Client, new_gift: dict[str, Any], old_gift: dict[str, Any]) -> None:
    sticker_msg_id = new_gift.get("sticker_msg_id")
    upgrade_msg_id = old_gift.get("upgrade_msg_id")
    if not sticker_msg_id or not upgrade_msg_id:
        return
    try:
        username = await get_released_peer(app, new_gift)
        text = compose_text(new_gift, username)
        link_preview = create_link_preview(new_gift, sticker_msg_id)
        await edit_msg(app, upgrade_msg_id, text, link_preview)
        logger.info("Upgrade notification updated for gift %s", new_gift["id"])
    except Exception:
        logger.exception("Failed to edit upgrade notification for gift %s", new_gift.get("id"))

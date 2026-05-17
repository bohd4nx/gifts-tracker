import logging
from typing import Any

from pyrogram import Client

from app.services.notifications.base import send_msg
from app.services.notifications.crafts import compose_text
from app.utils.gifts import create_link_preview, get_released_peer

logger = logging.getLogger(__name__)


async def notify_craft(app: Client, gift: dict[str, Any]) -> None:
    gift_id: int = gift["id"]
    sticker_msg_id = gift.get("sticker_msg_id")

    if not sticker_msg_id:
        logger.warning("No sticker_msg_id for craft notification of gift %s", gift_id)
        return

    try:
        variants = await app.get_gift_upgrade_variants(gift_id)  # type: ignore[attr-defined]
        new_count = len(variants.models)
        old_count = (gift.get("raw") or {}).get("models_count") or 0
        delta = new_count - old_count

        gift.setdefault("raw", {})["models_count"] = new_count

        if delta <= 0:
            logger.info("Craft detected for gift %s but delta=%d, skipping", gift_id, delta)
            return

        username = await get_released_peer(app, gift)
        text = compose_text(gift, delta, username)
        link_preview = create_link_preview(gift, sticker_msg_id)
        await send_msg(app, text, link_preview)
        logger.info("Craft notification sent for gift %s, delta=%d", gift_id, delta)
    except Exception:
        logger.exception("Failed to send craft notification for gift %s", gift_id)

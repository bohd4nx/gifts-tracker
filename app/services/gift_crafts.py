import logging
from typing import Any

from pyrogram import Client

from app.notifications.sender import send_notification

logger = logging.getLogger(__name__)


async def notify_craft_models_changed(app: Client, gift_data: dict[str, Any]) -> None:
    gift_id: int = gift_data.get("id")  # type: ignore[assignment]
    sticker_msg_id = gift_data.get("sticker_msg_id")
    if not sticker_msg_id:
        logger.warning(f"No sticker_msg_id for craft notification of gift {gift_id}")
        return
    try:
        variants = await app.get_gift_upgrade_variants(gift_id)  # type: ignore[attr-defined]
        new_count = len(variants.models)
        old_count = (gift_data.get("raw") or {}).get("models_count") or 0
        delta = new_count - old_count

        # persist new model count into gift_data so it's saved to DB
        gift_data.setdefault("raw", {})["models_count"] = new_count

        if delta <= 0:
            logger.info(f"Craft detected for gift {gift_id} but model delta={delta}, skipping notify")
            return

        await send_notification(app, gift_data, sticker_msg_id, is_craft=True, craft_delta=delta)
        logger.info(f"Sent craft notification for gift {gift_id}, models delta={delta}")
    except Exception:
        logger.exception(f"Failed to send craft notification for gift {gift_id}")

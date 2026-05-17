import asyncio
import logging
from typing import Any

from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.types import LinkPreviewOptions

from app.core import config
from app.utils import create_link_preview, get_released_peer

from .crafts import create_craft_message_text
from .gifts import create_gift_message_text
from .upgrades import create_upgrade_message_text

logger = logging.getLogger(__name__)


async def _send_or_edit(app: Client, text: str, link_preview: LinkPreviewOptions | None, message_id: int | None = None) -> int:
    """Sends a new channel message or edits an existing one; returns message_id."""
    if message_id:
        await app.edit_message_text(
            chat_id=config.CHANNEL_ID,
            message_id=message_id,
            text=text,
            link_preview_options=link_preview,  # type: ignore[arg-type]
        )
        return message_id

    message = await app.send_message(chat_id=config.CHANNEL_ID, text=text, link_preview_options=link_preview)  # type: ignore[arg-type]
    return message.id


async def _compose_message(
    app: Client,
    gift_data: dict[str, Any],
    sticker_message_id: int,
    is_upgrade: bool,
    is_craft: bool = False,
    craft_delta: int | None = None,
) -> tuple[str, LinkPreviewOptions | None]:
    """Builds message text and link preview for the given notification type."""
    username = await get_released_peer(app, gift_data)
    link_preview = create_link_preview(gift_data, sticker_message_id)
    if is_craft:
        text = create_craft_message_text(gift_data, craft_delta or 0, username)
    elif is_upgrade:
        text = create_upgrade_message_text(gift_data, username)
    else:
        text = create_gift_message_text(gift_data, username)
    return text, link_preview


async def send_notification(
    app: Client,
    gift_data: dict[str, Any],
    sticker_message_id: int,
    is_upgrade: bool = False,
    is_craft: bool = False,
    craft_delta: int | None = None,
) -> int | None:
    try:
        text, link_preview = await _compose_message(
            app,
            gift_data,
            sticker_message_id,
            is_upgrade,
            is_craft=is_craft,
            craft_delta=craft_delta,
        )
        return await _send_or_edit(app, text, link_preview)
    except FloodWait as e:
        # back off and retry transparently — the caller never sees FloodWait
        logger.warning(f"Flood wait triggered, sleeping for {e.value}s on gift {gift_data['id']}")
        await asyncio.sleep(e.value)
        return await send_notification(
            app,
            gift_data,
            sticker_message_id,
            is_upgrade,
            is_craft=is_craft,
            craft_delta=craft_delta,
        )
    except Exception as e:
        logger.exception(f"Failed to send notification for gift {gift_data['id']}: {e}")
        return None


async def edit_notification(
    app: Client,
    message_id: int,
    gift_data: dict[str, Any],
    sticker_message_id: int,
    is_upgrade: bool = False,
) -> bool:
    try:
        text, link_preview = await _compose_message(app, gift_data, sticker_message_id, is_upgrade)
        await _send_or_edit(app, text, link_preview, message_id)
        return True
    except FloodWait as e:
        logger.warning(f"Flood wait triggered, sleeping for {e.value}s while editing gift {gift_data['id']}")
        await asyncio.sleep(e.value)
        return await edit_notification(app, message_id, gift_data, sticker_message_id, is_upgrade)
    except Exception as e:
        if "MESSAGE_NOT_MODIFIED" not in str(e):
            logger.exception(f"Failed to edit notification for gift {gift_data['id']}: {e}")
        return False

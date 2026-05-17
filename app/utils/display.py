from typing import Any

from pyrogram.types import LinkPreviewOptions

from app.core import config


def gift_emoji(gift_data: dict[str, Any]) -> str:
    emoji_id = gift_data.get("emoji_id")
    if emoji_id:
        return f'<emoji id="{emoji_id}">🎁</emoji>'
    return "🎁"


def create_link_preview(gift_data: dict[str, Any], sticker_message_id: int) -> LinkPreviewOptions | None:
    raw_data = gift_data.get("raw", {})
    auction_slug = raw_data.get("auction_slug")

    if auction_slug and raw_data.get("auction"):
        return LinkPreviewOptions(
            url=f"https://t.me/auction/{auction_slug}",
            prefer_small_media=True,
            show_above_text=True,
        )

    if not sticker_message_id:
        return None

    return LinkPreviewOptions(
        url=f"https://t.me/{config.STICKERS_CHANNEL_USERNAME}/{sticker_message_id}",
        prefer_small_media=True,
        show_above_text=True,
    )


async def get_released_peer(app: Any, gift_data: dict[str, Any]) -> str | None:
    raw_data = gift_data.get("raw", {})
    released_by = raw_data.get("released_by")

    if not released_by or not isinstance(released_by, dict):
        return None

    peer_id = released_by.get("id")
    if not peer_id:
        return None

    try:
        # NOTE: currently gifts are released only by channels,
        # so peer_id is converted to a channel chat_id (-100...).
        # may require changes if users or groups start releasing gifts.
        chat_id = int(f"-100{peer_id}")
        chat = await app.get_chat(chat_id)
        return chat.username  # type: ignore[no-any-return]
    except Exception:
        return None

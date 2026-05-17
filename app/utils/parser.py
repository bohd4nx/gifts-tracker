import logging
from typing import Any

from pyrogram.file_id import FileId, FileType

from app.database.schemas import GiftsWrite

logger = logging.getLogger(__name__)


def parse_gift(gift: Any) -> GiftsWrite:
    sticker_file_id, sticker_raw = _parse_sticker(getattr(gift, "sticker", None), gift.id)

    return GiftsWrite(
        id=gift.id,
        price=gift.stars,
        upgrade_price=getattr(gift, "upgrade_stars", None),
        total_amount=getattr(gift, "availability_total", None),
        sticker_file_id=sticker_file_id,
        sticker_raw=sticker_raw,
        raw={
            "_": "StarGift",
            "title": getattr(gift, "title", None),
            "require_premium": getattr(gift, "require_premium", False),
            "limited_per_user": getattr(gift, "limited_per_user", False),
            "per_user_total": getattr(gift, "per_user_total", None),
            "locked_until_date": getattr(gift, "locked_until_date", None),
            "released_by": _parse_released_by(gift),
            "auction": getattr(gift, "auction", False),
            "auction_slug": getattr(gift, "auction_slug", None),
            "gifts_per_round": getattr(gift, "gifts_per_round", None),
            "upgrade_variants": getattr(gift, "upgrade_variants", None),
            "models_count": None,
        },
    )


def _parse_sticker(sticker: Any, gift_id: int) -> tuple[str | None, dict[str, Any] | None]:
    if not sticker:
        return None, None

    dc_id: int = getattr(sticker, "dc_id", 0)
    media_id: int = getattr(sticker, "id", 0)
    access_hash: int = getattr(sticker, "access_hash", 0)
    file_reference: bytes = getattr(sticker, "file_reference", b"")

    if not all([dc_id, media_id, access_hash, file_reference]):
        return None, None

    sticker_raw = {"dc_id": dc_id, "id": media_id, "access_hash": access_hash, "file_reference": file_reference}

    try:
        file_id = FileId(
            file_type=FileType.DOCUMENT,
            dc_id=dc_id,
            media_id=media_id,
            access_hash=access_hash,
            file_reference=file_reference,
        ).encode()
        return file_id, sticker_raw
    except Exception:
        logger.exception("Failed to encode file_id for gift %s", gift_id)
        return None, sticker_raw


def _parse_released_by(gift: Any) -> dict[str, Any] | None:
    peer = getattr(gift, "released_by", None)
    if not peer:
        return None
    return {
        "_": peer.__class__.__name__,
        "id": getattr(peer, "channel_id", getattr(peer, "user_id", None)),
    }

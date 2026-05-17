import asyncio
import logging
from typing import Any

from pyrogram import Client, raw
from pyrogram.errors import FloodWait

from app.core import config
from app.database import SessionLocal
from app.database.crud import update_gift_emoji_id
from app.methods import (
    add_sticker_to_set,
    create_sticker_set,
    get_sticker_set,
    make_sticker_item,
)

logger = logging.getLogger(__name__)


class PackState:
    ref: raw.types.InputStickerSetID | None = None


pack = PackState()


async def init_pack(app: Client) -> None:
    """Resolves the existing emoji pack by short name, or creates it from scratch."""
    try:
        stickerset = await get_sticker_set(
            app,
            raw.types.InputStickerSetShortName(short_name=config.EMOJI_PACK_SHORT_NAME),
        )
        pack.ref = raw.types.InputStickerSetID(
            id=stickerset.set.id,
            access_hash=stickerset.set.access_hash,
        )
        logger.info(f"Emoji pack ready: {stickerset.set.count} stickers in '{config.EMOJI_PACK_SHORT_NAME}'")
    except Exception:
        logger.info("Emoji pack not found — creating...")
        await build_emoji_pack(app, config.EMOJI_PACK_SHORT_NAME, config.EMOJI_PACK_TITLE)


async def add_gift_to_pack(app: Client, gift_data: dict[str, Any]) -> int | None:
    """Adds a gift sticker to the emoji pack via MTProto and returns the new emoji_id."""
    if pack.ref is None or not gift_data.get("sticker_raw"):
        return None

    try:
        result = await add_sticker_to_set(app, pack.ref, make_sticker_item(gift_data["sticker_raw"]))
        emoji_id = result.documents[-1].id
        await asyncio.sleep(1.5)
        return emoji_id
    except FloodWait as e:
        logger.warning(f"FloodWait {e.value}s — failed to add gift {gift_data['id']} to emoji pack")
        await asyncio.sleep(e.value)
        return None
    except Exception as e:
        logger.error(f"Failed to add gift {gift_data['id']} to emoji pack: {e}")
        return None


async def build_emoji_pack(app: Client, short_name: str, title: str) -> None:
    """Creates an emoji pack from all .tgs gifts and saves each emoji_id to DB."""
    me = await app.get_me()
    star_gifts: raw.types.payments.StarGifts = await app.invoke(raw.functions.payments.GetStarGifts(hash=0))  # type: ignore[arg-type]
    # keep only animated (.tgs) stickers; sort by last_sale_date so the pack order is stable
    gifts_sorted = sorted(
        (
            g
            for g in star_gifts.gifts
            if getattr(g, "sticker", None)
            and getattr(getattr(g, "sticker", None), "mime_type", "") == "application/x-tgsticker"
        ),
        key=lambda g: getattr(g, "last_sale_date", 0) or 0,
    )
    if not gifts_sorted:
        logger.error("No .tgs stickers found — cannot build emoji pack")
        return

    user_peer = await app.resolve_peer(me.id)
    # create the set with the first gift; the API requires at least one sticker at creation time
    first, *rest = gifts_sorted

    stickerset_ref, first_emoji_id = await create_sticker_set(
        app, user_peer, title, short_name, make_sticker_item(getattr(first, "sticker"))
    )
    pack.ref = stickerset_ref

    async with SessionLocal() as session:
        await update_gift_emoji_id(session, first.id, first_emoji_id)

    added, failed = 1, 0
    for gift in rest:
        try:
            result = await add_sticker_to_set(app, stickerset_ref, make_sticker_item(getattr(gift, "sticker")))
            emoji_id = result.documents[-1].id
            await asyncio.sleep(1.5)
            async with SessionLocal() as session:
                await update_gift_emoji_id(session, gift.id, emoji_id)
            added += 1
        except FloodWait as e:
            logger.warning(f"FloodWait {e.value}s — skipping gift {gift.id}")
            await asyncio.sleep(e.value)
            failed += 1
        except Exception as e:
            logger.error(f"Failed to add gift {gift.id} to emoji pack: {e}")
            failed += 1

    msg = f"Added {added}/{len(gifts_sorted)} emojis to emoji pack"
    logger.info(msg if not failed else f"{msg} ({failed} failed)")

import asyncio
import logging

from pyrogram import Client, raw
from pyrogram.errors import FloodWait

from app.database import SessionLocal
from app.database.crud import update_gift_emoji_id

from . import state
from .sticker_set import add_sticker_to_set, create_sticker_set, make_sticker_item

logger = logging.getLogger(__name__)


async def create_emoji_pack(app: Client, short_name: str, title: str) -> None:
    me = await app.get_me()
    star_gifts: raw.types.payments.StarGifts = await app.invoke(
        raw.functions.payments.GetStarGifts(hash=0)  # type: ignore[arg-type]
    )

    animated_gifts = sorted(
        (
            g
            for g in star_gifts.gifts
            if getattr(g, "sticker", None)
            and getattr(getattr(g, "sticker", None), "mime_type", "") == "application/x-tgsticker"
        ),
        key=lambda g: getattr(g, "last_sale_date", 0) or 0,
    )

    if not animated_gifts:
        logger.error("No .tgs stickers found — cannot create emoji pack")
        return

    user_peer = await app.resolve_peer(me.id)
    first, *rest = animated_gifts

    stickerset_ref, first_emoji_id = await create_sticker_set(
        app, user_peer, title, short_name, make_sticker_item(getattr(first, "sticker"))
    )
    state.pack_ref = stickerset_ref

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
            logger.warning("FloodWait %ds — skipped gift %s", e.value, gift.id)
            await asyncio.sleep(e.value)
            failed += 1
        except Exception:
            logger.exception("Failed to add gift %s to emoji pack", gift.id)
            failed += 1

    summary = f"Added {added}/{len(animated_gifts)} emojis to emoji pack"
    logger.info(summary if not failed else "%s (%d failed)", summary, failed)

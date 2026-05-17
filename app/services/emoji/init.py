import logging

from pyrogram import Client, raw

from app.core import config

from . import state
from .build import create_emoji_pack
from .sticker_set import get_sticker_set

logger = logging.getLogger(__name__)


async def init_emoji_pack(app: Client) -> None:
    try:
        stickerset = await get_sticker_set(
            app,
            raw.types.InputStickerSetShortName(short_name=config.EMOJI_PACK_SHORT_NAME),
        )
        state.pack_ref = raw.types.InputStickerSetID(
            id=stickerset.set.id,
            access_hash=stickerset.set.access_hash,
        )
        logger.info("Emoji pack ready: %d stickers in '%s'", stickerset.set.count, config.EMOJI_PACK_SHORT_NAME)
    except Exception:
        logger.info("Emoji pack not found — creating...")
        await create_emoji_pack(app, config.EMOJI_PACK_SHORT_NAME, config.EMOJI_PACK_TITLE)

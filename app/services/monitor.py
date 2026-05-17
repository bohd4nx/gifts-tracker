import asyncio
import logging

from aiogram import Bot
from pyrogram import Client
from pyrogram.errors import FloodWait

from app.core import config
from app.database import SessionLocal
from app.database.crud import get_all_gifts, row_to_schema, upsert_gifts

from .emoji_pack import init_pack
from .new_gift import process_gifts

logger = logging.getLogger(__name__)


async def run_gift_monitor(app: Client, bot: Bot) -> None:
    """Main polling loop: loads history from DB, fetches Telegram gifts, saves changes."""
    cycle_count = 0
    last_hash = 0

    await init_pack(app)

    while True:
        try:
            cycle_count += 1
            logger.info(f"Starting gift check cycle #{cycle_count}")

            async with SessionLocal() as session:
                gifts = await get_all_gifts(session)
                gifts_history = {gift.id: row_to_schema(gift).to_dict() for gift in gifts}

                has_changes, last_hash = await process_gifts(app, bot, gifts_history, last_hash)
                if has_changes:
                    await upsert_gifts(session, list(gifts_history.values()))

            await asyncio.sleep(config.INTERVAL)
        except FloodWait as e:
            logger.warning(f"Flood wait triggered, sleeping for {e.value}s")
            await asyncio.sleep(e.value)
        except Exception:
            logger.exception("Unexpected error in gift monitor loop")
            await asyncio.sleep(config.INTERVAL)

import asyncio
from pathlib import Path

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from pyrogram import Client, enums
from pyrogram.errors import AuthKeyDuplicated, AuthKeyUnregistered, SessionRevoked
from pyrogram.types import LinkPreviewOptions

from app.core import config, logger, setup_logging
from app.database import close_db, init_db
from app.services import run_gift_monitor


async def main() -> None:
    setup_logging()
    await init_db()
    logger.info("Database initialized")

    client = Client(
        name="GiftsTracker",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        phone_number=config.PHONE_NUMBER,
        password=config.PASSWORD or "",
        device_model="PC 64bit",
        system_version="Windows 10",
        app_version="6.8.2 x64",
        lang_pack="tdesktop",
        lang_code="en",
        workdir=str(Path(__file__).parent / "session"),
        client_platform=enums.ClientPlatform.DESKTOP,
        plugins=dict(root="app.commands"),
        parse_mode=enums.ParseMode.HTML,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        skip_updates=True,
        workers=8,
        sleep_threshold=30,
        max_concurrent_transmissions=10,
    )

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True),
    )

    async with client as app:
        me = await app.get_me()
        logger.info(f"Logged in as @{me.username or ''} [{me.id}]")

        try:
            await run_gift_monitor(app, bot)
        finally:
            await bot.session.close()
            await close_db()
            logger.info("Application shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (AuthKeyUnregistered, AuthKeyDuplicated, SessionRevoked):
        logger.error("Authorization error: Session expired or invalid. Please re-authenticate.")
    except (KeyboardInterrupt, SystemExit):
        logger.info("Program successfully terminated")
    except Exception as ex:
        logger.exception(f"Unexpected error: {ex}")

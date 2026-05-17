import time
from datetime import UTC, datetime

from pyrogram import Client
from pyrogram.raw.functions import Ping
from pyrogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import config
from app.core.constants import STATUS_EMOJIS
from app.database import with_session
from app.database.crud import count_gifts
from app.utils import format_uptime

STARTED_AT = datetime.now(UTC)


@with_session
async def handle_status(client: Client, message: Message, session: AsyncSession) -> None:
    total_gifts = await count_gifts(session)

    start_time = time.time()
    await client.invoke(Ping(ping_id=0))
    ping_ms = round((time.time() - start_time) * 1000, 2)

    uptime_delta = datetime.now(UTC) - STARTED_AT
    uptime_str = format_uptime(uptime_delta)
    dc_id = getattr(getattr(client, "session", None), "dc_id", "Unknown")

    e = STATUS_EMOJIS
    status_text = (
        f"{e['header']} <b>Gifts Tracker Status</b>\n\n"
        f"{e['datacenter']} <b>Datacenter:</b> "
        f'<a href="https://docs.pyrogram.org/faq/what-are-the-ip-addresses-of-telegram-data-centers">DC{dc_id}</a> [<code>{ping_ms} ms</code>]\n'
        f"{e['uptime']} <b>Uptime:</b> <code>{uptime_str}</code>\n"
        f"{e['interval']} <b>Interval:</b> <code>{config.INTERVAL}s</code>\n"
        f"{e['total_gifts']} <b>Total gifts in DB:</b> <code>{total_gifts}</code>"
    )

    await message.edit_text(status_text)

from typing import Any

from sqlalchemy import func, or_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Gifts
from app.database.schemas import GiftsRead, GiftsWrite
from app.utils import deserialize_json, serialize_json

_SYNC_FIELDS = (
    "price",
    "upgrade_price",
    "total_amount",
    "sticker_file_id",
    "sticker_msg_id",
    "msg_id",
    "upgrade_msg_id",
    "emoji_id",
)


async def get_all_gifts(session: AsyncSession) -> list[Gifts]:
    result = await session.execute(select(Gifts))
    return list(result.scalars())


async def count_gifts(session: AsyncSession) -> int:
    result = await session.execute(select(func.count()).select_from(Gifts))
    return result.scalar_one()


async def get_gift_by_msg_id(session: AsyncSession, msg_id: int) -> tuple[Gifts | None, bool]:
    """Returns (row, is_upgrade). Uses a single OR query on indexed columns."""
    result = await session.execute(select(Gifts).where(or_(Gifts.msg_id == msg_id, Gifts.upgrade_msg_id == msg_id)).limit(1))
    row = result.scalar_one_or_none()
    if row is None:
        return None, False
    return row, row.msg_id != msg_id


async def update_gift_emoji_id(session: AsyncSession, gift_id: int, emoji_id: int) -> None:
    await session.execute(update(Gifts).where(Gifts.id == gift_id).values(emoji_id=emoji_id))
    await session.commit()


async def upsert_gifts(session: AsyncSession, gifts: list[dict[str, Any] | GiftsWrite]) -> None:
    if not gifts:
        return

    payloads = [g if isinstance(g, GiftsWrite) else GiftsWrite.from_dict(g) for g in gifts]

    rows = [
        {
            "id": p.id,
            **{field: getattr(p, field) for field in _SYNC_FIELDS},
            "sticker_raw": serialize_json(p.sticker_raw),
            "raw_data": serialize_json(p.raw),
        }
        for p in payloads
    ]

    stmt = insert(Gifts).values(rows)
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],
        set_={col: stmt.excluded[col] for col in _SYNC_FIELDS}
        | {
            "sticker_raw": stmt.excluded.sticker_raw,
            "raw_data": stmt.excluded.raw_data,
            "last_updated": func.now(),
        },
    )
    await session.execute(stmt)
    await session.commit()


def row_to_schema(gift: Gifts) -> GiftsRead:
    return GiftsRead(
        id=gift.id,
        price=gift.price,
        upgrade_price=gift.upgrade_price,
        total_amount=gift.total_amount,
        sticker_file_id=gift.sticker_file_id,
        sticker_msg_id=gift.sticker_msg_id,
        msg_id=gift.msg_id,
        upgrade_msg_id=gift.upgrade_msg_id,
        emoji_id=gift.emoji_id,
        sticker_raw=deserialize_json(gift.sticker_raw) if gift.sticker_raw else {},
        raw=deserialize_json(gift.raw_data),
    )

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Gifts(Base):
    __tablename__ = "gifts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    upgrade_price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sticker_file_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sticker_raw: Mapped[str | None] = mapped_column(Text, nullable=True)
    sticker_msg_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    msg_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    upgrade_msg_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    emoji_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    raw_data: Mapped[str | None] = mapped_column(Text, nullable=True)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        index=True,
    )

    __table_args__ = (
        # lookup by msg_id / upgrade_msg_id — used in get_by_msg_id
        Index("ix_gifts_msg_id", "msg_id"),
        Index("ix_gifts_upgrade_msg_id", "upgrade_msg_id"),
    )

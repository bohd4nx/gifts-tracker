from dataclasses import dataclass, field
from typing import Any


@dataclass
class GiftsWrite:
    id: int
    price: int | None = None
    upgrade_price: int | None = None
    total_amount: int | None = None
    sticker_file_id: str | None = None
    sticker_msg_id: int | None = None
    msg_id: int | None = None
    upgrade_msg_id: int | None = None
    emoji_id: int | None = None
    sticker_raw: dict[str, Any] | None = None
    raw: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GiftsWrite":
        return cls(
            id=data["id"],
            price=data.get("price"),
            upgrade_price=data.get("upgrade_price"),
            total_amount=data.get("total_amount"),
            sticker_file_id=data.get("sticker_file_id"),
            sticker_msg_id=data.get("sticker_msg_id"),
            msg_id=data.get("msg_id"),
            upgrade_msg_id=data.get("upgrade_msg_id"),
            emoji_id=data.get("emoji_id"),
            sticker_raw=data.get("sticker_raw"),
            raw=data.get("raw"),
        )


@dataclass
class GiftsRead:
    id: int
    price: int | None = None
    upgrade_price: int | None = None
    total_amount: int | None = None
    sticker_file_id: str | None = None
    sticker_msg_id: int | None = None
    msg_id: int | None = None
    upgrade_msg_id: int | None = None
    emoji_id: int | None = None
    sticker_raw: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "_": "Gift",
            "id": self.id,
            "price": self.price,
            "upgrade_price": self.upgrade_price,
            "total_amount": self.total_amount,
            "sticker_file_id": self.sticker_file_id,
            "sticker_msg_id": self.sticker_msg_id,
            "msg_id": self.msg_id,
            "upgrade_msg_id": self.upgrade_msg_id,
            "emoji_id": self.emoji_id,
            "sticker_raw": self.sticker_raw,
            "raw": self.raw,
        }

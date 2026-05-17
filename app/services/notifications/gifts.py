from typing import Any

from app.core.constants import EMOJIS, FOOTER
from app.utils import format_number, gift_emoji

_e = EMOJIS


def compose_text(gift: dict[str, Any], username: str | None = None) -> str:
    raw = gift.get("raw", {})

    lines = [
        f"{gift_emoji(gift)} <b>New gift available</b>\n",
        f"{_e['gift_id']} <b>ID:</b> <code>{gift['id']}</code>",
    ]

    if username:
        lines.append(f"{_e['released_by']} <b>Released by:</b> @{username}")

    price_line = f"{_e['price']} <b>Price:</b> <code>{format_number(gift['price'])}</code>{_e['stars']}"
    if total := gift.get("total_amount"):
        price_line += f" • <b>Supply:</b> <code>{format_number(total)}</code>"
    lines.append(price_line)

    if raw.get("auction") and (per_round := raw.get("gifts_per_round")):
        rounds = (gift.get("total_amount") or 0) // per_round
        lines.append(f"{_e['auction_rounds']} <b>{rounds}</b> rounds • <b>{per_round}</b> per round")

    limits = []
    if raw.get("require_premium"):
        limits.append("<b>Premium Only</b>")
    if per_user := raw.get("per_user_total"):
        limits.append(f"<b>{per_user}</b> per user")
    if limits:
        lines.append(f"{_e['premium']} {' • '.join(limits)}")

    if raw.get("locked_until_date"):
        lines.append(f"{_e['restrictions']} <b>Time Locked</b>")

    lines.append(f"\n{FOOTER}")
    return "\n".join(lines)

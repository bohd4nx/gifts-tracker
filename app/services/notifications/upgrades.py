from typing import Any

from app.core.constants import EMOJIS, FOOTER
from app.utils import format_number, gift_emoji

_e = EMOJIS


def compose_text(gift: dict[str, Any], username: str | None = None) -> str:
    lines = [
        f"{gift_emoji(gift)} <b>Gift upgrade available</b>\n",
        f"{_e['gift_id']} <b>ID:</b> <code>{gift['id']}</code>",
    ]

    if username:
        lines.append(f"{_e['released_by']} <b>Released by:</b> @{username}")

    upgrade_price = format_number(gift.get("upgrade_price") or 0)
    lines.append(f"{_e['upgrade_price']} <b>Upgrade Price:</b> <code>{upgrade_price}</code> {_e['stars']}")

    lines.append(f"\n{FOOTER}")
    return "\n".join(lines)

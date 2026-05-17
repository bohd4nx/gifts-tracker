from typing import Any

from app.core.constants import EMOJIS, FOOTER
from app.utils import gift_emoji

_e = EMOJIS


def compose_text(gift: dict[str, Any], delta: int, username: str | None = None) -> str:
    lines = [
        f"{gift_emoji(gift)} <b>Gift craft available</b> • {delta} models\n",
        f"{_e['gift_id']} <b>ID:</b> <code>{gift['id']}</code>",
    ]

    if username:
        lines.append(f"{_e['released_by']} <b>Released by:</b> @{username}")

    lines.append(f"\n{FOOTER}")
    return "\n".join(lines)

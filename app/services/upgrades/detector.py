from typing import Any


def detect_upgrade_available(old_gift: dict[str, Any], new_gift: dict[str, Any]) -> bool:
    old = old_gift.get("upgrade_price")
    new = new_gift.get("upgrade_price")
    return old is None and new is not None and new > 0


def detect_upgrade_price_changed(old_gift: dict[str, Any], new_gift: dict[str, Any]) -> bool:
    old = old_gift.get("upgrade_price")
    new = new_gift.get("upgrade_price")
    return old is not None and new is not None and old != new and bool(old_gift.get("upgrade_msg_id"))

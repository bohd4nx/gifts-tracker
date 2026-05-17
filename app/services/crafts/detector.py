from typing import Any


def detect_models_change(old_gift: dict[str, Any], new_gift: dict[str, Any]) -> int | None:
    old_val = (old_gift.get("raw") or {}).get("upgrade_variants")
    new_val = (new_gift.get("raw") or {}).get("upgrade_variants")
    if old_val is not None and new_val is not None and new_val > old_val:
        return int(new_val) - int(old_val)
    return None

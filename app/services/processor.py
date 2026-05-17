import logging
from typing import Any

from aiogram import Bot
from pyrogram import Client

from app.services.crafts import detect_models_change, notify_craft
from app.services.gifts import fetch_gifts, process_new_gifts
from app.services.upgrades import (
    detect_upgrade_available,
    detect_upgrade_price_changed,
    notify_upgrade_available,
    notify_upgrade_price_changed,
)

logger = logging.getLogger(__name__)

_MSG_ID_KEYS = ("msg_id", "sticker_msg_id", "upgrade_msg_id", "emoji_id")


async def process_gifts(
    app: Client, bot: Bot, gifts_history: dict[int, dict[str, Any]], last_hash: int = 0
) -> tuple[bool, int]:
    new_hash, current_gifts = await fetch_gifts(app, last_hash)
    if current_gifts is None:
        return False, new_hash

    new_ids = current_gifts.keys() - gifts_history.keys()
    new_gifts = {k: current_gifts[k] for k in new_ids}
    existing_gifts = {k: v for k, v in current_gifts.items() if k not in new_ids}

    changed = bool(new_gifts)
    if new_gifts:
        logger.info("%d new gift(s) detected", len(new_gifts))
        await process_new_gifts(app, bot, new_gifts, gifts_history)

    changed |= await _check_existing_gifts(app, existing_gifts, gifts_history)
    return changed, new_hash


async def _check_existing_gifts(
    app: Client,
    current_gifts: dict[int, dict[str, Any]],
    gifts_history: dict[int, dict[str, Any]],
) -> bool:
    changed = False
    for gift_id, current_gift in current_gifts.items():
        if gift_id not in gifts_history:
            continue
        old_gift = gifts_history[gift_id]
        _carry_message_ids(old_gift, current_gift)
        if await _dispatch_change(app, old_gift, current_gift):
            changed = True
        gifts_history[gift_id] = current_gift
    return changed


def _carry_message_ids(old_gift: dict[str, Any], new_gift: dict[str, Any]) -> None:
    for key in _MSG_ID_KEYS:
        if key in old_gift:
            new_gift[key] = old_gift[key]


async def _dispatch_change(app: Client, old_gift: dict[str, Any], new_gift: dict[str, Any]) -> bool:
    if detect_upgrade_available(old_gift, new_gift):
        await notify_upgrade_available(app, new_gift)
        return True
    if detect_upgrade_price_changed(old_gift, new_gift):
        await notify_upgrade_price_changed(app, new_gift, old_gift)
        return True
    if detect_models_change(old_gift, new_gift):
        await notify_craft(app, new_gift)
        return True
    return False

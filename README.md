<div align="center">

# Telegram Gifts Tracker

[![Stars](https://img.shields.io/github/stars/bohd4nx/GiftsTracker?style=flat&color=blue&label=Stars)](https://github.com/bohd4nx/GiftsTracker/stargazers)
[![Forks](https://img.shields.io/github/forks/bohd4nx/GiftsTracker?style=flat&color=blue&label=Forks)](https://github.com/bohd4nx/GiftsTracker/forks)
[![Telegram](https://img.shields.io/badge/channel-@GiftsTracker-blue?style=flat&logo=telegram)](https://t.me/GiftsTracker)

Userbot that monitors new Telegram gifts, upgrade events, and craft events — sends rich notifications and maintains a custom emoji pack.

**[Follow Channel](https://t.me/GiftsTracker)** · **[Report Bug](https://github.com/bohd4nx/GiftsTracker/issues)**

</div>

---

## Features

- Detects new gifts in the Telegram store and sends rich notifications
- Monitors upgrade availability and tracks price changes on upgradeable gifts
- Tracks gift crafts and notifies when crafting events occur
- Uploads gift stickers to a dedicated channel for animated link previews
- Automatically builds and maintains a custom Telegram emoji pack
- Stores full gift history in PostgreSQL via async SQLAlchemy
- `.status` command — shows DC, ping, polling interval and total gifts in DB

---

## Quick Start

**Requires:** Python 3.12+, PostgreSQL

```bash
git clone https://github.com/bohd4nx/GiftsTracker.git
cd GiftsTracker
cp .env.example .env   # fill in credentials
```

```bash
# Docker (recommended)
# First run must be interactive — the userbot will ask for a login code
docker compose run --rm app

# After login the session is saved. Start normally:
docker compose up -d

# or local
pip install -e .
python main.py
```

---

## Configuration

| Variable                    | Required | Default | Description                                     |
| --------------------------- | -------- | ------- | ----------------------------------------------- |
| `DATABASE_URL`              | ✅       | —       | PostgreSQL connection string                    |
| `PHONE_NUMBER`              | ✅       | —       | Telegram account phone number                   |
| `PASSWORD`                  | —        | —       | 2FA password (if enabled)                       |
| `BOT_TOKEN`                 | ✅       | —       | Token from [@BotFather](https://t.me/BotFather) |
| `CHANNEL_ID`                | ✅       | —       | Channel to send gift notifications              |
| `STICKERS_CHANNEL_ID`       | ✅       | —       | Channel to upload gift stickers                 |
| `STICKERS_CHANNEL_USERNAME` | ✅       | —       | Username of the stickers channel                |
| `EMOJI_PACK_SHORT_NAME`     | ✅       | —       | Short name of the custom emoji pack             |
| `EMOJI_PACK_TITLE`          | ✅       | —       | Display title of the custom emoji pack          |
| `API_ID`                    | —        | `2040`  | Telegram API ID (from my.telegram.org)          |
| `API_HASH`                  | —        | —       | Telegram API hash                               |
| `INTERVAL`                  | —        | `15.0`  | Polling interval in seconds                     |

---

## Docker Commands

```bash
docker compose logs -f          # live logs
docker compose restart          # restart
docker compose down             # stop & remove
docker compose up -d --build    # rebuild & restart
```

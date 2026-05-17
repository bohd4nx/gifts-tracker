<div align="center">

<h1>Telegram Gifts Tracker</h1>

<p><b>Userbot that monitors new Telegram gifts, upgrade events and craft events — sends notifications and maintains a custom emoji pack.</b></p>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Channel-@GiftsTracker-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://t.me/GiftsTracker)
[![Donate](https://img.shields.io/badge/Donate-TON-0098EA?style=flat&logo=ton&logoColor=white)](https://app.tonkeeper.com/transfer/UQCppfw5DxWgdVHf3zkmZS8k1mt9oAUYxQLwq2fz3nhO8No5)

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

## Installation

```bash
git clone https://github.com/bohd4nx/GiftsTracker.git
cd GiftsTracker
pip install -e .
cp .env.example .env
```

Fill in `.env` with your configuration (see `.env.example`), then:

```bash
python main.py
```

---

## Docker

**First run** must be interactive so the userbot can ask for the login code:

```bash
docker compose run --rm app
```

After login the session is saved to the project root. Press `Ctrl+C` to stop, then start normally:

```bash
docker compose up -d
```

Useful commands:

```bash
docker compose logs -f         # live logs
docker compose restart         # restart
docker compose down            # stop & remove
docker compose up -d --build   # rebuild & restart
```

---

## License

This project is provided as-is for educational purposes.

---

<div align="center">

### Made with ❤️ by [@bohd4nx](https://t.me/bohd4nx)

**Star ⭐ this repo if you found it useful!**

</div>

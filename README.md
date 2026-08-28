# Byte Tap — Backend

FastAPI backend for **Byte Tap**, a tap-to-earn Telegram Mini App. Handles player data, tap logic, and energy regeneration, backed by SQLite.

## Features

- **Player management** — auto-creates a player record on first request
- **Tap-to-earn mechanics** — balance and energy tracked per player
- **Energy regeneration** — energy recovers over time, calculated server-side from elapsed seconds
- **Anti-cheat batch tap validation** — the client sends batched tap counts; the server independently recalculates how many taps the player's energy could actually support, so the client can never report more than what's physically possible
- **Static file serving** — serves the game's frontend (`byte-tap.html`) directly

## Tech stack

- **Python 3.13**
- **FastAPI** — web framework
- **SQLite** — data storage (via the built-in `sqlite3` module, no ORM)
- **Passenger (via cPanel Python Selector)** — WSGI deployment on shared hosting, bridged with [a2wsgi](https://github.com/abersheeran/a2wsgi)

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/game` | Serves the game frontend |
| `GET` | `/player/{telegram_id}` | Get or create a player, with regenerated energy |
| `POST` | `/player/{telegram_id}/tap` | Register a single tap |
| `POST` | `/player/{telegram_id}/tap-batch?taps=N` | Register a batch of taps (used by the frontend's optimistic UI) |

## Project structure

```
main.py              # FastAPI app and routes
database.py           # SQLite access layer
passenger_wsgi.py     # WSGI entrypoint for Passenger/cPanel deployment
byte-tap.html          # Game frontend (served by the backend)
requirements.txt      # Python dependencies
```

## Running locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## Related

- [byte-tap-bot](https://github.com/OleksandrHabelchenko/byte-tap-bot) — the Telegram bot that launches this Mini App

## Try it

[Open the bot on Telegram](https://t.me/Byte_tap_bot) and tap "Play Game" to try it live.


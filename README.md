# Full Telegram Support for Spam Filtering

A Telegram Bot API project that detects and moderates spam in group chats.

## Features
- Rule-based spam scoring (links, repeats, keywords, unicode tricks)
- Safe actions: delete, warn, mute (optional)
- Allowlist for trusted users
- Configurable thresholds and rules

## Quick Start
1. Create a bot with @BotFather and copy the token.
2. Add the bot to your group and promote it to admin with delete/mute rights.
3. Set up environment variables.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with your token
python -m bot.main
```

## Configuration
See `bot/config.py` and `.env.example` for available settings.

## Project Structure
- `bot/` Core bot code
- `docs/` Design notes and threat model
- `tests/` Placeholder for tests

## Notes
- The bot only moderates groups it is added to.
- For privacy, only minimal message data is kept in memory.

## License
MIT

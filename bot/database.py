import aiosqlite
from datetime import datetime, timezone

async def init_db():
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                user_id INTEGER PRIMARY KEY,
                count INTEGER DEFAULT 0
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS moderation_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                chat_id INTEGER NOT NULL,
                message_text TEXT,
                base_score INTEGER DEFAULT 0,
                profile_score INTEGER DEFAULT 0,
                final_score INTEGER DEFAULT 0,
                reasons TEXT,
                action_taken TEXT NOT NULL
            )
        """)
        await db.commit()

async def increment_warning(user_id: int) -> int:
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute(
            "INSERT INTO warnings (user_id, count) VALUES (?, 1) "
            "ON CONFLICT(user_id) DO UPDATE SET count = count + 1",
            (user_id,)
        )
        await db.commit()
        async with db.execute("SELECT count FROM warnings WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else 0

async def reset_warnings(user_id: int):
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("DELETE FROM warnings WHERE user_id = ?", (user_id,))
        await db.commit()


async def log_moderation_event(
    user_id: int,
    chat_id: int,
    message_text: str,
    base_score: int,
    profile_score: int,
    final_score: int,
    reasons: list[str],
    action_taken: str,
):
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute(
            """
            INSERT INTO moderation_events (
                created_at, user_id, chat_id, message_text,
                base_score, profile_score, final_score, reasons, action_taken
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                user_id,
                chat_id,
                message_text,
                base_score,
                profile_score,
                final_score,
                ", ".join(reasons),
                action_taken,
            ),
        )
        await db.commit()

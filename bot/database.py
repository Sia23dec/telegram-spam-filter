import aiosqlite

async def init_db():
    async with aiosqlite.connect("bot_data.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                user_id INTEGER PRIMARY KEY,
                count INTEGER DEFAULT 0
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

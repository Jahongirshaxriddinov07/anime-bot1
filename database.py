import asyncpg
from config import DATABASE_URL

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=DATABASE_URL)
        await self.create_tables()

    async def create_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    full_name VARCHAR(255),
                    age INT,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS channels (
                    channel_id BIGINT PRIMARY KEY,
                    invite_link TEXT NOT NULL
                );
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS animes (
                    code VARCHAR(50) PRIMARY KEY,
                    message_id BIGINT NOT NULL,
                    title TEXT
                );
            """)

    async def add_user(self, user_id: int, full_name: str, age: int):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO users (user_id, full_name, age) VALUES ($1, $2, $3) ON CONFLICT (user_id) DO UPDATE SET full_name = $2, age = $3",
                user_id, full_name, age
            )

    async def get_user(self, user_id: int):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)

    async def add_channel(self, channel_id: int, invite_link: str):
        async with self.pool.acquire() as conn:
            await conn.execute("INSERT INTO channels (channel_id, invite_link) VALUES ($1, $2) ON CONFLICT (channel_id) DO UPDATE SET invite_link = $2", channel_id, invite_link)

    async def get_channels(self):
        async with self.pool.acquire() as conn:
            return await conn.fetch("SELECT * FROM channels")

    async def delete_channel(self, channel_id: int):
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM channels WHERE channel_id = $1", channel_id)

    async def add_anime(self, code: str, message_id: int, title: str = None):
        async with self.pool.acquire() as conn:
            await conn.execute("INSERT INTO animes (code, message_id, title) VALUES ($1, $2, $3) ON CONFLICT (code) DO UPDATE SET message_id = $2, title = $3", code, message_id, title)

    async def get_anime(self, code: str):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM animes WHERE code = $1", code)

    async def get_random_anime(self):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM animes ORDER BY RANDOM() LIMIT 1")

    async def get_stats(self):
        async with self.pool.acquire() as conn:
            total = await conn.fetchval("SELECT COUNT(*) FROM users")
            active = await conn.fetchval("SELECT COUNT(*) FROM users WHERE is_active = TRUE")
            return {"total": total, "active": active}

db = Database()

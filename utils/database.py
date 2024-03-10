import asyncpg

from config import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT


async def get_db_connection():
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

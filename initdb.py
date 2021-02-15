import asyncio

from db import DATABASE_URI, db


async def main():
    await db.set_bind(DATABASE_URI)
    await db.gino.create_all()
    await db.pop_bind().close()


asyncio.get_event_loop().run_until_complete(main())

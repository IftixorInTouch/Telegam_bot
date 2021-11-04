from users import Database
import asyncio


async def test():
    db = Database()
    await db.create_pool()
    await db.drop_user(0)
loop = asyncio.get_event_loop()
app = loop.run_until_complete(test())

import asyncio
import asyncpg
import logging
from config import PGHOST, PG_PASS, PG_USER

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


async def create_db():
    create_db_command = open('create_db.sql', 'r').read()
    logging.info('Connecting to db')

    conn: asyncpg.connection = await asyncpg.connect(
        user=PG_USER,
        password=PG_PASS,
        host=PGHOST
    )
    await conn.execute(create_db_command)
    logging.info('Table has been created')
    await conn.close()

async def create_pool():
    return await asyncpg.create_pool(
        user=PG_USER,
        password=PG_PASS,
        host=PGHOST
    )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
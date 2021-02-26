import asyncio

import aiohttp
from aiopg.sa import create_engine
from db import log, create_table


async def get_resp():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://www.dsdev.tech/logs/20210123') as resp:
            resp_json = await resp.json()
            for log in resp_json['logs']:
                yield {
                    'date': log['created_at'],
                    'user_id': log['user_id'],
                    'first_name': log['first_name'],
                    'last_name': log['second_name'],
                    'message': log['message']
                }


async def main():
    async with create_engine(database='postgres',
                             user='postgres',
                             password='1234',
                             host='localhost',
                             port=5432) as engine:

        await create_table(engine)
        async with engine.acquire() as conn:
            values = get_resp()
            while True:
                try:
                    l = await values.__anext__()
                    await conn.execute(
                        log.insert().values(
                            date=l['date'],
                            user_id=l['user_id'],
                            first_name=l['first_name'],
                            last_name=l['last_name'],
                            message=l['message'])
                    )
                except StopAsyncIteration:
                    print('ВСЕ')
                    break


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
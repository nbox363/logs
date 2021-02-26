import asyncio
import re

import aiohttp
from aiopg.sa import create_engine

from db import log_table, create_table
from sort import quick_sort


async def get_resp():
    data = []
    async with aiohttp.ClientSession() as session:
        async with session.get('http://www.dsdev.tech/logs/20210123') as resp:
            resp_json = await resp.json()
            for log in resp_json['logs']:
                data.append(
                    {
                        'date': log['created_at'],
                        'new': re.sub('\D', '', log['created_at']),
                        'user_id': log['user_id'],
                        'first_name': log['first_name'],
                        'last_name': log['second_name'],
                        'message': log['message']
                    }
                )

    quick_sort(data)
    return data


async def main():
    async with create_engine(database='postgres',
                             user='postgres',
                             password='1234',
                             host='localhost',
                             port=5432) as engine:

        await create_table(engine)

        async with engine.acquire() as conn:
            logs = await get_resp()
            for log in logs:
                await conn.execute(
                    log_table.insert().values(
                        date=log['date'],
                        user_id=log['user_id'],
                        first_name=log['first_name'],
                        last_name=log['last_name'],
                        message=log['message'])
                )


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
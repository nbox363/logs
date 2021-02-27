import asyncio
import re

import aiohttp
from aiopg.sa import create_engine

from db import log_table, create_table
from sort import quick_sort


class LogHandler:

    def __init__(self):
        self.url = 'http://www.dsdev.tech/logs/' + '20210123'
        self.logs = []

    async def main(self):
        resp_json = await self.get_resp()
        self.get_logs(resp_json)
        self.sorting(self.logs)
        await self.write_db()

    async def get_resp(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                resp_json = await resp.json()
                return resp_json

    def get_logs(self, resp_json) -> None:
        for log in resp_json['logs']:
            self.logs.append({
                'date': log['created_at'],
                'new': re.sub('\D', '', log['created_at']),
                'user_id': log['user_id'],
                'first_name': log['first_name'],
                'last_name': log['second_name'],
                'message': log['message']}
            )

    async def write_db(self):
        async with create_engine(database='postgres',
                                 user='postgres',
                                 password='1234',
                                 host='localhost') as engine:
            await create_table(engine)

            async with engine.acquire() as conn:
                for log in self.logs:
                    await self.insert_tbl(
                        conn,
                        date=log['date'],
                        user_id=log['user_id'],
                        first_name=log['first_name'],
                        last_name=log['last_name'],
                        message=log['message'])

    @staticmethod
    async def insert_tbl(conn, **kwargs) -> None:
        await conn.execute(log_table.insert().values(**kwargs))

    @staticmethod
    def sorting(seq: list) -> None:
        quick_sort(seq)


l = LogHandler()
loop = asyncio.get_event_loop()
loop.run_until_complete(l.main())

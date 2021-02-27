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
        resp_json = await self.get_resp_json()
        self.get_logs(resp_json)
        self.sorting(self.logs)
        await self.write_db()

    async def get_resp_json(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                resp_json = await resp.json()
                return resp_json

    def get_logs(self, resp_json) -> None:
        for log in resp_json['logs']:
            log['new'] = re.sub('\D', '', log['created_at'])
            self.logs.append(log)

    async def write_db(self):
        async with create_engine(database='postgres',
                                 user='postgres',
                                 password='1234',
                                 host='localhost') as engine:
            await create_table(engine)

            async with engine.acquire() as conn:
                for log in self.logs:
                    log.pop('new')
                    await self.insert_tbl(conn, log)

    @staticmethod
    async def insert_tbl(conn, log) -> None:
        await conn.execute(log_table.insert().values(**log))

    @staticmethod
    def sorting(seq: list) -> None:
        quick_sort(seq)


l = LogHandler()
loop = asyncio.get_event_loop()
loop.run_until_complete(l.main())
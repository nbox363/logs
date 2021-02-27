import re
from abc import ABC, abstractmethod

import psycopg2
import requests
from requests.models import Response

from db import create_table, drop_table, insert_table
from sort import quick_sort


class ABCResp(ABC):
    @abstractmethod
    def json(self) -> dict:
        pass


class ABCRequestsClient(ABC):
    @abstractmethod
    def get(self, str) -> ABCResp:
        pass


class RequestsClient(ABCRequestsClient):
    def get(self, str) -> Response:
        return requests.get(str)


class LogHandler:

    def __init__(self, req: ABCRequestsClient):
        self.req = req

    def main(self, data):
        resp = self.req.get(self.url(data))
        logs = resp.json()['logs']
        logs_for_sort = self.add_num(logs)
        logs_after_sort = self.sorting(logs_for_sort)
        self.safe(logs_after_sort)

    def safe(self, logs):
        conn = psycopg2.connect(database='postgres',
                                user='postgres',
                                password='1234',
                                host='localhost')

        cur = conn.cursor()
        cur.execute(drop_table())
        cur.execute(create_table())
        for log in logs:
            cur.execute(insert_table(),
                        (log['created_at'], log['user_id'], log['first_name'], log['second_name'], log['message']))
        cur.close()
        conn.commit()

    def sorting(self, logs):
        quick_sort(logs)
        return logs

    def add_num(self, logs: list):
        for log in logs:
            log['new'] = re.sub('\D', '', log['created_at'])
        return logs

    def url(self, data):
        url = 'http://www.dsdev.tech/logs/' + data  # '20210123'
        return url


r = RequestsClient()
l = LogHandler(r)
l.main('20210123')

import logging
import re
import sys
from abc import ABC, abstractmethod

import psycopg2
import requests
from requests.models import Response

from db import create_table, drop_table, insert_table
from utilities import months, quick_sort

logging.basicConfig(level=logging.DEBUG)


class ABCResp(ABC):
    @abstractmethod
    def json(self) -> dict:
        pass


class ABCRequestsClient(ABC):
    @abstractmethod
    def get(self, url) -> ABCResp:
        pass


class RequestsClient(ABCRequestsClient):
    def get(self, url) -> Response:
        return requests.get(url)


class LogHandler:

    def __init__(self, req: ABCRequestsClient):
        self.req = req

    def main(self, data):
        logging.debug(f'Method "main" was called with date {" ".join(data)}')

        resp = self.req.get(self.url(data))

        try:
            logs = resp.json()['logs']
            logs_for_sort = self.add_num(logs)
            logs_after_sort = self.sorting(logs_for_sort)
            self.safe(logs_after_sort)
        except KeyError:
            error = resp.json()['error']
            logging.debug(error)

    @staticmethod
    def safe(logs):
        conn = psycopg2.connect(database='postgres',
                                user='postgres',
                                password='1234',
                                host='localhost')

        cur = conn.cursor()
        cur.execute(drop_table())
        cur.execute(create_table())

        for log in logs:
            fields = [val for key, val in log.items() if key != 'date_num']
            cur.execute(insert_table(), fields)

        cur.close()
        conn.commit()

    @staticmethod
    def sorting(logs):
        quick_sort(logs)
        return logs

    @staticmethod
    def add_num(logs: list):
        for log in logs:
            log['date_num'] = re.sub('\D', '', log['created_at'])
        return logs

    @staticmethod
    def url(data):
        url = 'http://www.dsdev.tech/logs/' + data[2] + months[data[1]] + data[0]
        return url


if __name__ == '__main__':
    req = RequestsClient()
    l = LogHandler(req)
    if sys.argv[1:]:
        l.main(sys.argv[1:])
    else:
        l.main(['23', 'февраля', '2021'])

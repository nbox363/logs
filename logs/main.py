import logging
import re
import sys

from abc_classes import *
from db import insert, drop, create
from utilities import months, quick_sort, default_date

logging.basicConfig(level=logging.DEBUG)


class LogHandler:

    def __init__(self, req: ABCRequestsClient, psycopg2: ABCPsycopgClient):
        self.req = req
        self.psycopg2 = psycopg2

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

    def safe(self, logs):
        conn = self.psycopg2.connect(
            database='postgres',
            user='postgres',
            password='1234',
            host='localhost')

        print(type(conn))

        cur = conn.cursor()
        cur.execute(drop)
        cur.execute(create)

        for log in logs:
            fields = [str(val) for key, val in log.items() if key != 'date_num']
            cur.execute(insert, fields)

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
    conn = ConnClient()
    l = LogHandler(req, conn)
    if sys.argv[1:]:
        l.main(sys.argv[1:])
    else:
        l.main(default_date)

import logging
import re
import sys

from abc_classes import *
from db import insert, get_connect, get_cursor
from utilities import months, quick_sort, default_date

logging.basicConfig(level=logging.DEBUG)


class LogHandler:

    def __init__(self, req: ABCRequestsClient):
        self.req = req

    def main(self, data):
        logging.debug(f'Method "main" was called with date {" ".join(data)}')

        resp = self.req.get(self.url(data))
        resp_json = resp.json()

        conn = get_connect()
        cur = get_cursor(conn)

        if resp_json['error']:
            error = resp.json()['error']
            logging.debug(error, 'Даты не существует')
        else:
            logs = resp.json()['logs']
            logs_for_sort = self.add_date_num(logs)
            logs_after_sort = self.sorting(logs_for_sort)
            self.safe(logs_after_sort, cur)

        cur.close()
        conn.commit()

    @staticmethod
    def safe(logs, cur):
        for log in logs:
            fields = [str(val) for key, val in log.items() if key != 'date_num']
            cur.execute(insert, fields)

    @staticmethod
    def sorting(logs):
        quick_sort(logs)
        return logs

    @staticmethod
    def add_date_num(logs: list):
        for log in logs:
            log['date_num'] = re.sub('\D', '', log['created_at'])
        return logs

    @staticmethod
    def url(data):
       return 'http://www.dsdev.tech/logs/' + data[2] + months[data[1]] + data[0]


if __name__ == '__main__':
    req = RequestsClient()
    log_handler = LogHandler(req)
    if sys.argv[1:]:
        log_handler.main(sys.argv[1:])
    else:
        log_handler.main(default_date)

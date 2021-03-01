import logging
import re
import sys

from db import insert, ABCDbConn, PGConn
from req import *
from utilities import months, quick_sort, default_date

logging.basicConfig(level=logging.DEBUG)


class LogHandler:

    def __init__(self, req: ABCRequestsClient, conn: ABCDbConn):
        self.req = req
        self.conn = conn

    def main(self, data: list):
        logging.debug(f'Method "main" was called with date {" ".join(data)}')

        resp = self.req.get(self.url(data))
        resp_json = resp.json()

        if resp_json['error']:
            logging.debug(resp.json()['error'], 'Даты не существует')
            return

        logs = resp.json()['logs']
        logs_for_sort = self.add_date_num(logs)
        logs_after_sort = self.sorting(logs_for_sort)

        self.conn.init_db()
        self.save(logs_after_sort)
        self.conn.commit()

    def save(self, logs: list):
        for log in logs:
            fields = [str(val) for key, val in log.items() if key != 'date_num']
            self.conn.execute(insert, fields)

    @staticmethod
    def sorting(logs: list):
        quick_sort(logs)
        return logs

    @staticmethod
    def add_date_num(logs: list):
        for log in logs:
            log['date_num'] = re.sub('\D', '', log['created_at'])
        return logs

    @staticmethod
    def url(data: list):
        return 'http://www.dsdev.tech/logs/' + data[2] + months[data[1]] + data[0]


if __name__ == '__main__':
    req = RequestsClient()
    conn = PGConn()
    log_handler = LogHandler(req, conn)
    if sys.argv[1:]:
        log_handler.main(sys.argv[1:])
    else:
        log_handler.main(default_date)

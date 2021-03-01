import unittest
from unittest.mock import Mock, MagicMock

from main import LogHandler
from req import RequestsClient

req = RequestsClient()

test_date = ['22', 'февраля', '2021']
expected_url = 'http://www.dsdev.tech/logs/20210222'

unsorted_data = [
    {'created_at': '2021-02-22T14:48:35',
     'date_num': '3'},
    {'created_at': '2021-02-22T08:16:11',
     'date_num': '2'},
    {'created_at': '2021-02-22T19:51:28',
     'date_num': '1'}
]

sorted_data = [
    {'created_at': '2021-02-22T19:51:28',
     'date_num': '1'},
    {'created_at': '2021-02-22T08:16:11',
     'date_num': '2'},
    {'created_at': '2021-02-22T14:48:35',
     'date_num': '3'},
]


class TestLogHandler(unittest.TestCase):

    def test_url(self):
        self.assertEqual(LogHandler.url(test_date), expected_url)

    def test_sorting(self):
        self.assertEqual(LogHandler.sorting(unsorted_data), sorted_data)

    def test_save(self):
        data = [{'created_at': '2021-02-22T00:04:18',
              'date_num': '20210222000418'},
             {'created_at': '2021-02-22T00:16:45',
              'date_num': '20210222001645'}]

        connMock = Mock()
        connMock.execute = MagicMock()
        real = LogHandler(req, connMock)
        real.save(data)
        count = connMock.execute.call_count

        self.assertEqual(len(data), count)


if __name__ == '__main__':
    unittest.main()

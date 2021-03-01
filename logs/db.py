from abc import ABC, abstractmethod

import psycopg2


class ABCDbConn(ABC):
    @abstractmethod
    def init_db(self):
        pass

    @abstractmethod
    def execute(self, s, *args):
        pass

    @abstractmethod
    def commit(self):
        pass


class PGConn(ABCDbConn):
    def __init__(self):
        self.conn = psycopg2.connect(
            database='postgres',
            user='postgres',
            password='1234',
            host='localhost')

    def init_db(self):
        cur = self.conn.cursor()
        cur.execute('DROP TABLE IF EXISTS log')
        cur.execute('''CREATE TABLE log (id serial PRIMARY KEY,
                                         created_at TIMESTAMP,
                                         first_name VARCHAR(155),
                                         message TEXT,
                                         second_name VARCHAR(155),
                                         user_id INT)''')
        cur.close()

    def execute(self, s, *args):
        cursor = self.conn.cursor()
        cursor.execute(s, args)
        cursor.close()

    def commit(self):
        pass


insert = '''INSERT INTO log (created_at, first_name, message, second_name, user_id)
            VALUES (%s, %s, %s, %s, %s);'''

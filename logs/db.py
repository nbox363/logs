import psycopg2


def get_connect():
    conn = psycopg2.connect(
        database='postgres',
        user='postgres',
        password='1234',
        host='localhost')
    return conn


def get_cursor(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS log')
    cur.execute('''CREATE TABLE log (id serial PRIMARY KEY,
                                   created_at TIMESTAMP,
                                   first_name VARCHAR(155),
                                   message TEXT,
                                   second_name VARCHAR(155),
                                   user_id INT)''')
    return cur


insert = '''INSERT INTO log (created_at, first_name, message, second_name, user_id)
            VALUES (%s, %s, %s, %s, %s);'''

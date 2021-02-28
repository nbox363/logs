def insert_table() -> str:
    command = '''INSERT INTO log (created_at, first_name, message, second_name, user_id)
                  VALUES (%s, %s, %s, %s, %s);'''
    return command


def drop_table() -> str:
    command = 'DROP TABLE IF EXISTS log'
    return command


def create_table() -> str:
    command = '''CREATE TABLE log (id serial PRIMARY KEY,
                                   created_at TIMESTAMP,
                                   first_name VARCHAR(155),
                                   message TEXT,
                                   second_name VARCHAR(155),
                                   user_id INT)'''
    return command
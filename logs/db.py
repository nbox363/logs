def insert_table() -> str:
    command = '''INSERT INTO log (created_at, first_name, message, second_name, user_id)
                  VALUES (%s, %s, %s, %s, %s);'''
    return command


def drop_table() -> str:
    command = 'DROP TABLE IF EXISTS log'
    return command


def create_table() -> str:
    command = '''CREATE TABLE log (id serial PRIMARY KEY,
                                   created_at Date,   
                                   user_id INT,
                                   first_name varchar(155),
                                   second_name varchar(155),
                                   message TEXT)'''
    return command
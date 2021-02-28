insert = '''INSERT INTO log (created_at, first_name, message, second_name, user_id)
                  VALUES (%s, %s, %s, %s, %s);'''

drop = 'DROP TABLE IF EXISTS log'

create = '''CREATE TABLE log (id serial PRIMARY KEY,
                                   created_at TIMESTAMP,
                                   first_name VARCHAR(155),
                                   message TEXT,
                                   second_name VARCHAR(155),
                                   user_id INT)'''

import sqlalchemy as sa
from sqlalchemy.sql.ddl import CreateTable

meta = sa.MetaData()

log_table = sa.Table(
    'log_table', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('created_at', sa.DateTime, nullable=False),
    sa.Column('user_id', sa.Integer, nullable=False),
    sa.Column('first_name', sa.String(155), nullable=False),
    sa.Column('second_name', sa.String(155), nullable=False),
    sa.Column('message', sa.Text, nullable=False),
    # Indexes #
    sa.PrimaryKeyConstraint('id', name='log_id_pkey')
)


def insert_table():
    command = '''INSERT INTO log (created_at, user_id, first_name, second_name, message)
                  VALUES (%s, %s, %s, %s, %s);'''
    return command


def drop_table():
    command = 'DROP TABLE IF EXISTS log'
    return command


def create_table():
    command = '''CREATE TABLE log (id serial PRIMARY KEY,
                                   created_at Date,   
                                   user_id INT,
                                   first_name varchar(155),
                                   second_name varchar(155),
                                   message TEXT)'''
    return command
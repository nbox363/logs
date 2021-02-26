import sqlalchemy as sa

meta = sa.MetaData()

log_table = sa.Table(
    'log', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('date', sa.DateTime, nullable=False),
    sa.Column('user_id', sa.Integer, nullable=False),
    sa.Column('first_name', sa.String(155), nullable=False),
    sa.Column('last_name', sa.String(155), nullable=False),
    sa.Column('message', sa.Text, nullable=False),

    # Indexes #
    sa.PrimaryKeyConstraint('id', name='log_id_pkey')
)


async def create_table(engine):
    async with engine.acquire() as conn:
        await conn.execute('DROP TABLE IF EXISTS log_table')
        await conn.execute(
            '''CREATE TABLE log_table (id SERIAL PRIMARY KEY,
                                       date TIMESTAMP,   
                                       user_id INT,
                                       first_name VARCHAR(155),
                                       last_name VARCHAR(155),
                                       message TEXT)''')

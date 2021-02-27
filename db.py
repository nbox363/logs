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


async def create_table(engine):
    async with engine.acquire() as conn:
        await conn.execute('DROP TABLE IF EXISTS log_table')
        await conn.execute(CreateTable(log_table))

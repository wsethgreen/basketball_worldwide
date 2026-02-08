from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine import URL


# TODO: Update when implementing DB
db_url = URL.create(
    drivername="postgresql+asyncpg",
    username="TODO",
    password="TODO",
    host="localhost",
    port=5432,
    database="project",
)

engine = create_async_engine(db_url)

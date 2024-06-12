from contextlib import asynccontextmanager
from api import router
from database import get_config as get_db_config
from database import get_connection, start, teardown
from fastapi import FastAPI
from settings.settings import settings
from tortoise.contrib.fastapi import register_tortoise


@asynccontextmanager
async def lifespan(_: FastAPI):
    await start(conn=get_db_config(get_connection()))

    yield
    await teardown()


app = FastAPI(title='Meme Storage', lifespan=lifespan, debug=settings.prod_mode)


app.include_router(router)
register_tortoise(app=app, config=get_db_config(get_connection()), generate_schemas=True)

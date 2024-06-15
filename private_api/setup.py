from private_api.api import router
from fastapi import FastAPI
from settings.settings import settings


app = FastAPI(title='S3 Interactions', debug=settings.prod_mode)
app.include_router(router)

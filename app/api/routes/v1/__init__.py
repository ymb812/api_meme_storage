from fastapi import APIRouter
from api.routes.v1.meme import router as bots_users_router

router = APIRouter()
router.include_router(bots_users_router, prefix='/memes', tags=['memes'])

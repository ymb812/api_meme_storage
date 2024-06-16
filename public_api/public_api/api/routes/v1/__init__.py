from fastapi import APIRouter
from public_api.api.routes.v1.meme_handlers import router as meme_router

router = APIRouter()
router.include_router(meme_router, prefix='/memes', tags=['memes'])

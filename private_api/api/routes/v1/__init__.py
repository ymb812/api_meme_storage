from fastapi import APIRouter
from private_api.api.routes.v1.media_handlers import router as image_router

router = APIRouter()
router.include_router(image_router, prefix='/media', tags=['media'])

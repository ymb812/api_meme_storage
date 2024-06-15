from fastapi import APIRouter
from private_api.api.routes import router as api_router

router = APIRouter()
router.include_router(api_router, prefix='/sapi')

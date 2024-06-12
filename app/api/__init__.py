from fastapi import APIRouter
from api.routes import router as api_router
#from api.internal_routes import router as internal_api_router

router = APIRouter()
router.include_router(api_router, prefix='/api')
#router.include_router(internal_api_router, prefix='/sapi')

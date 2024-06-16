from fastapi import APIRouter
from private_api.api.routes.v1 import router as router_v1

router = APIRouter()
router.include_router(router_v1, prefix='/v1')

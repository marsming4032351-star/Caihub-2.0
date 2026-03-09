from fastapi import APIRouter

from app.api.v1.endpoints.dishes import router as dishes_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.production import router as production_router
from app.api.v1.endpoints.standards import router as standards_router
from app.api.v1.endpoints.system import router as system_router
from app.api.v1.endpoints.vision import router as vision_router

router = APIRouter()
router.include_router(health_router, tags=["health"])
router.include_router(dishes_router, prefix="/dishes", tags=["dishes"])
router.include_router(production_router, prefix="/production", tags=["production"])
router.include_router(standards_router, prefix="/standards", tags=["standards"])
router.include_router(system_router, prefix="/system", tags=["system"])
router.include_router(vision_router, prefix="/vision", tags=["vision"])

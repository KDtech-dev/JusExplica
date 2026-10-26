from fastapi import APIRouter

from app.api.routes import catalog, explanations, health
from app.core.config import settings


api_router = APIRouter()

api_router.include_router(health.router)

api_router.include_router(
    explanations.router,
    prefix=settings.api_prefix,
)
api_router.include_router(
    catalog.router,
    prefix=settings.api_prefix,
)
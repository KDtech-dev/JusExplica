from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.service_name,
    description=settings.service_description,
    version=settings.service_version,
)


@app.get("/", tags=["Health"])
def home():
    return {
        "success": True,
        "message": "Serviço Python do JusExplica está funcionando.",
    }


app.include_router(api_router)
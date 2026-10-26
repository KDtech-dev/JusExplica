from fastapi import APIRouter, HTTPException

from app.services.tpu_catalog_service import (
    CatalogUnavailableError,
    search_movement_by_code,
)


router = APIRouter(
    prefix="/catalog",
    tags=["Catalog"],
)


@router.get("/movements/{code}")
def get_movement_by_code(code: str):
    if not code.strip():
        raise HTTPException(
            status_code=400,
            detail="Informe o código da movimentação.",
        )

    try:
        movements = search_movement_by_code(code)

    except CatalogUnavailableError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    return {
        "success": True,
        "source": "CNJ - Sistema de Gestão de Tabelas Processuais Unificadas",
        "query": {
            "type": "movement",
            "code": code,
        },
        "found": bool(movements),
        "data": movements,
    }
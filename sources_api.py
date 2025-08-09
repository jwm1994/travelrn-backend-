from fastapi import APIRouter
from app.sources import REGISTRY

router = APIRouter(prefix="/sources", tags=["sources"])

@router.get("")
def list_sources():
    return {"count": len(REGISTRY), "sources": list(REGISTRY.keys())}

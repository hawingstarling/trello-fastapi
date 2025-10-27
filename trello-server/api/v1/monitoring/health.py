from fastapi import APIRouter
from app.schemas.extras.health import Health
from core.config import config

health_router = APIRouter()

@health_router.get("/", response_model=Health)
async def health() -> Health:
  return Health(version=config.RELEASE_VERSION, status="Healthy")
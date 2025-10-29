from fastapi import Depends, FastAPI, Request
from api import router

from core.config import config
from core.logger import setup_logger

logger = setup_logger("server")

def init_routers(app_: FastAPI) -> None:
  app_.include_router(router)

def create_app() -> FastAPI:
  app_ = FastAPI(
    title="TrelloServer tutorial",
    description="TrelloServer by @odin",
    version="1.0.0",
    docs_url=None if config.ENVIRONMENT == "production" else "/docs"
  )
  init_routers(app_=app_)

  logger.info("FastAPI application created")

  return app_

app = create_app()
from fastapi import Depends, FastAPI, Request
from core.config import config
from api import router

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

  return app_

app = create_app()
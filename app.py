from typing import Optional

import uvicorn
from fastapi import FastAPI
from omegaconf import OmegaConf, DictConfig

from src.containers.conainers import AppContainer
from src.routes.routers import router as app_router
from src.routes import satellite_img as satellite_routes

def create_app() -> FastAPI:
    cfg = OmegaConf.load('config/config.yml')
    container = AppContainer()
    container.config.from_dict(cfg)
    container.wire([satellite_routes])
    app = FastAPI()
    set_routers(app)
    return app


def set_routers(app: FastAPI):
    app.include_router(app_router, prefix='/planets', tags=['planets'])

if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, port=2444, host='0.0.0.0')

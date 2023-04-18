from fastapi import FastAPI
from conf.config import settings
from fastapi.middleware.cors import CORSMiddleware


def register_middleware(app: FastAPI) -> None:
    if settings.MIDDLEWARE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

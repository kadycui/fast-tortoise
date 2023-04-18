from fastapi import FastAPI
from conf.config import settings
from tortoise.contrib.fastapi import register_tortoise

db_config = {
    'connections': {
        'default': {
            'engine': f'tortoise.backends.{settings.DB_ENGINE}',
            'credentials': {
                'host': f'{settings.DB_HOST}',
                'port': f'{settings.DB_PORT}',
                'user': f'{settings.DB_USER}',
                'password': f'{settings.DB_PASSWORD}',
                'database': f'{settings.DB_DATABASE}',
                'charset': f'{settings.DB_ENCODING}',
                'echo': f'{settings.DB_ECHO}'
            }
        },
    },
    'apps': {
        'models': {
            'models': [
                "models.user",
                "models.server"
            ],
            'default_connection': 'default',
        },
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}


def register_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        config=db_config,
        generate_schemas=settings.GENERATE_SCHEMAS,
        add_exception_handlers=settings.DB_ADD_EXCEPTION_HANDLERS
    )



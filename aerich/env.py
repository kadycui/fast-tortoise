import sys
sys.path.append('../')

from common.database import db_config
TORTOISE_ORM = {
    "connections": db_config['connections'],
    "apps": {
        "models": {
            "models": ["aerich.models",
                       "models.user",
                       "models.server"],
            "default_connection": "default",
        },
    },
}

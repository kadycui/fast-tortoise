import sys
from fastapi import FastAPI
from aioredis import Redis, TimeoutError, AuthenticationError
from conf.config import settings
from common.logger import logger


class RedisCli(Redis):
    def __init__(self):
        super(RedisCli, self).__init__(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            decode_responses=True  # 转码 utf-8
        )

    async def init_redis_connect(self):
        try:
            await self.ping()
        except TimeoutError:
            logger.error("redis连接超时")
            sys.exit()
        except AuthenticationError:
            logger.error("redis认证失败")
            sys.exit()
        except Exception as e:
            logger.error(f"redis连接异常{str(e)}")
            sys.exit()


redis_client = RedisCli()


def register_redis(app: FastAPI):
    @app.on_event("startup")
    async def startup_event():
        # 连接redis
        await redis_client.init_redis_connect()

    @app.on_event("shutdown")
    async def shutdown_event():
        # 关闭redis连接
        redis_client.init_redis_connect().close()

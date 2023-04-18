import os
from typing import Optional
from functools import lru_cache
from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    TITLE: Optional[str] = "fast-tortoise"
    VERSION = "v0.1.0"
    DESC: Optional[str] = """
    - FastGms, 基于FastAPI + TortoiseORM的后台系统
    - 实现： FastAPI
    """

    # Token
    TOKEN_ALGORITHM: str = 'HS256'
    TOKEN_SECRET_KEY: str = 'OSyMFBndkXFlymAA3pqtEakgZl-3nKUbjoe6PfCsXzA'  # 密钥(py生成方法：print(secrets.token_urlsafe(32)))
    TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3  # 单位：m

    # 日志文件路径
    BASE_PATH = Path(__file__).resolve().parent.parent
    LOG_PATH = os.path.join(BASE_PATH, 'logs')

    # 中间件
    MIDDLEWARE_CORS: bool = True

    # DB
    DB_ADD_EXCEPTION_HANDLERS: bool = True  # 线上环境请使用 False
    DB_ENGINE: str = "mysql"
    DB_ECHO: bool = True  # 是否显示SQL语句
    DB_HOST: str = '124.220.3.231'
    DB_PORT: int = 3336
    DB_USER: str = 'root'
    DB_PASSWORD: str = '123456'
    DB_DATABASE: str = 'fast_gms'
    DB_ENCODING: str = 'utf8mb4'
    
    # ORM
    GENERATE_SCHEMAS: bool = False

    # Redis
    REDIS_HOST: str = '10.16.168.61'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = '123456'
    REDIS_DATABASE: int = 0
    REDIS_TIMEOUT: int = 10

    # 静态文件
    STATIC_FILE: bool = True
    STATIC_PATH = os.path.join(BASE_PATH, 'static')

    # Docs
    DOCS_URL: str = '/docs'
    OPENAPI_URL: str = '/openapi'
    REDOCS_URL: str = None
   



@lru_cache
def get_settings():
    """ 读取配置优化写法 """
    return Settings()


settings = get_settings()

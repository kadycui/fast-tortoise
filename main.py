import uvicorn
from fastapi import FastAPI
from views import register_router
from conf.config import settings
from common.database import register_db
from common.redis import register_redis
from common import register_static_file, register_docs
from middleware.cors import register_middleware
from fastapi_pagination import add_pagination

app = FastAPI(
    description=settings.DESC,
    version=settings.VERSION,
    docs_url=None,
    redoc_url=None

)

# 静态文件注册
register_static_file(app)

# 使用本地docs静态文件
register_docs(app)

# 注册中间件
register_middleware(app)

# 注册路由
register_router(app)

# 数据库连接
register_db(app)

# 连接redis
# register_redis(app)

# 注册分页
add_pagination(app)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True, debug=True)

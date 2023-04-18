from fastapi import FastAPI
from views.user import user
from views.server import server
from views.channel import channel
from views.group import group
from views.notice import notice


def register_router(app: FastAPI) -> None:
    app.include_router(user, prefix="/api/user", tags=["用户认证"])
    app.include_router(server, prefix="/api/server", tags=["服务器"])
    app.include_router(channel, prefix="/api/channel", tags=["渠道"])
    app.include_router(group, prefix="/api/group", tags=["分区"])
    app.include_router(notice, prefix="/api/notice", tags=["公告"])

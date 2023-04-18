from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Depends
from tortoise.expressions import Q
from models.server import Server
from schemas.channel import ResChannelServers
from schemas.server import ResServers, ResOneServer, Server_Pydantic, ServerIn_Pydantic, ResQueryServer
from utils import Response200
from common.logger import logger
from control.server_operate import server_db

server = APIRouter()


@server.post("/", summary="创建一个服务器", response_model=ResOneServer)
async def create_one_server(server: Server_Pydantic):
    logger.info(f"创建一个服务器-{server.id}")
    ser_obj = await Server.create(**server.dict(exclude_unset=True))
    # data= await Server_Pydantic.from_tortoise_orm(ser_obj)
    return Response200(data=ser_obj)


@server.get("", summary="服务器查询", response_model=ResChannelServers)
async def server_query(s_keyword: Optional[str] = None, start_time: Optional[str] = None,
                       end_time: Optional[str] = None):
    if s_keyword and start_time and end_time:
        logger.info("关键字+开始时间+结束时间")
        if s_keyword.isdigit():
            data = await Server.filter(
                Q(Q(id=int(s_keyword)) | Q(name__contains=s_keyword) | Q(alias__contains=s_keyword)) & Q(
                    Q(create_time__gte=start_time) & Q(create_time__lte=end_time)))
        else:
            data = await Server.filter(
                Q(create_time__gte=start_time) | Q(create_time__lte=end_time) |
                Q(name__contains=s_keyword) | Q(alias__contains=s_keyword))
    elif s_keyword and not start_time and not end_time:
        logger.info("关键字")
        if s_keyword.isdigit():
            data = await Server.filter(
                Q(id=int(s_keyword)) | Q(name__contains=s_keyword) | Q(alias__contains=s_keyword))
        else:
            data = await Server.filter(Q(name__contains=s_keyword) | Q(alias__contains=s_keyword))
    elif start_time and end_time and not s_keyword:
        logger.info("开始时间+结束时间")
        data = await Server.filter(Q(create_time__gte=start_time) & Q(create_time__lte=end_time))
    else:
        logger.info("其他条件")
        data = []
    dic = {}
    for s in data:
        chs = await s.channels
        for c in chs:
            if c.name in list(dic.keys()):
                value = dic[c.name]
                value.append(s)
                dic[c.name] = value
            else:
                value = [s]
                dic[c.name] = value
    logger.info(dic)
    data = dic

    return Response200(data=data)


@server.get("/all", summary="获取所有服务器", response_model=ResServers)
async def get_all_server(request: Request):
    logger.info("获取所有服务器")
    all_server = await Server.all()
    data = {"other": all_server[0:1000],
            "publish": all_server[1001:5000],
            "xunxian": all_server[5001:8000],
            "jingling": all_server[8000:]}
    return Response200(data=data)


@server.put("/{server_id}", summary="更新一个服务器", response_model=ResOneServer)
async def update_one_server(server_id: int, server: ServerIn_Pydantic):
    logger.info(f"更新一个服务器-{server_id}")
    await Server.filter(id=server_id).update(**server.dict(exclude_unset=True))

    # 返回更新后的模型数据
    data = await Server_Pydantic.from_queryset_single(Server.get(id=server_id))
    return Response200(data=data)


@server.get("/{server_id}", summary="单个服务器信息", response_model=ResOneServer)
async def get_one_server(server_id: int):
    logger.info(f"获取单个服务器信息-{server_id}")
    s = await server_db.get_server_by_id(pk=server_id)
    # # print(Server_Pydantic.schema_json(indent=4))
    #
    # p1 = await Server_Pydantic.from_tortoise_orm(Server.get(id=server_id))
    # print(p1.json())
    #
    # p2 = await Server_Pydantic_List.from_queryset(Server.all())
    # print(p2.json())
    # print(p2.dict())
    return Response200(data=s)


@server.delete("/{server_id}", summary="删除一个服务器", response_model=ResOneServer)
async def delete_one_server(server_id: int):
    logger.info(f"删除一个服务器-{server_id}")
    data = await server_db.delete_one(server_id)
    return Response200(data=data)


@server.get("/make_json/server", summary="生成服务器json", response_model=Response200)
async def make_server_json():
    logger.info(f"生成服务器json")
    data = "生成完成"
    return Response200(data=data)


@server.get("/make_json/channel/{channel_id}", summary="生成单个渠道服务器json", response_model=Response200)
async def make_one_channel_json(channel_id: int):
    logger.info(f"生成单个渠道服务器json")
    data = "生成完成"
    return Response200(data=data)

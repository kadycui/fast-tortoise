import datetime
import hashlib
import json
import os
import time
import aiofiles
from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from tortoise.functions import Count

from models.server import Channel, Server, Group
from schemas.channel import ResChannels, Channel_Pydantic, ResOneChannel, ChannelIn_Pydantic, ResChannelServers
from schemas.server_list import ChannelJson, server_group_name, LogicServer
from utils import Response200
from common.logger import logger
from control.server_operate import server_db
from tortoise.expressions import Q
from conf.config import settings

channel = APIRouter()


@channel.post("/", summary="创建一个渠道", response_model=ResOneChannel)
async def create_one_channel(channel: Channel_Pydantic):
    logger.info(f"创建一个服务器-{channel.id}")
    ch_obj = await Channel.create(**channel.dict(exclude_unset=True))
    # data= await Channel_Pydantic.from_tortoise_orm(ch_obj)
    return Response200(data=ch_obj)


@channel.get("/all", summary="获取所有渠道", response_model=ResChannels)
async def get_all_channel():
    logger.info("获取所有渠道")
    all_channel = await Channel.all()
    return Response200(data=all_channel)


@channel.get("/{channel_id}", summary="获取一个渠道信息", response_model=ResOneChannel)
async def get_one_channel(channel_id: int, cid: Optional[str] = None, sid: Optional[str] = None,
                          start_time: Optional[str] = None, end_time: Optional[str] = None):
    logger.info(f"获取一个渠道信息-{channel_id}")
    # "GET /api/channel/channels_servers/all?cid=&sid=&start_time=2022-09-01+00:00:00&end_time=2022-09-01+23:59:59 HTTP/1.0"
    print(channel_id, sid, cid, start_time, end_time)
    now = "2022-08-01 14:52:14"
    dt = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    ct = await Channel.filter(create_time__gte=dt)
    print(ct)
    logger.info(f"当前日期的渠道{ct[0].id}-{ct[0].name}")

    c = await Channel.get(id=channel_id)
    return Response200(data=c)


@channel.put("/{channel_id}", summary="更新一个渠道", response_model=ResOneChannel)
async def update_one_channel(channel_id: int, channel: ChannelIn_Pydantic):
    logger.info(f"更新一个渠道-{channel_id}")
    await Channel.filter(id=channel_id).update(**channel.dict(exclude_unset=True))

    # 返回更新后的模型数据
    data = await Channel_Pydantic.from_queryset_single(Channel.get(id=channel_id))
    return Response200(data=data)


@channel.delete("/{channel_id}", summary="删除一个服渠道", response_model=ResOneChannel)
async def delete_one_channel(channel_id: int):
    logger.info(f"删除一个服渠道-{channel_id}")
    del_channel = await Channel.filter(id=channel_id)
    if not del_channel:
        raise HTTPException(
            status_code=404, detail=f'Channel {channel_id} not found')
    else:
        channel = del_channel[0]
        await channel.delete()
    return Response200(data=channel)


@channel.get("/channels_servers/all", summary="获取所有渠道下的服务器", response_model=ResChannelServers)
async def get_channels_servers(cid: Optional[str] = None, sid: Optional[str] = None, start_time: Optional[str] = None,
                               end_time: Optional[str] = None):
    # st = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    # et = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    # print(st, et)
    data = {}
    if sid:
        s = await Server.get(id=int(sid))
        cs = await s.channel
        for c in cs:
            data[c.name] = [s]
    elif cid:
        c = await Channel.filter(id=int(cid))
        if c:
            ch = c[0]
            data[ch.name] = await ch.server.all()
        else:
            data = []
    elif start_time and end_time:
        channels = await Channel.filter(Q(create_time__gte=start_time) & Q(create_time__lte=end_time))
        logger.info(f"在时间范围内的渠道--{channels}")
        if channels:
            for ch in channels:
                data[ch.name] = await ch.server.all()
    else:
        channels = await Channel.all()
        for ch in channels:
            data[ch.name] = await ch.server.all()
    return Response200(data=data)


@channel.get("/channel_servers/{channel_id}", summary="获取单个渠道下的服务器", response_model=ResChannelServers)
async def get_channel_servers(channel_id: int):
    data = {}
    channel = await Channel.get(id=channel_id)
    data[channel.name] = await channel.server.all()
    return Response200(data=data)


@channel.get("/make_server_list/", summary="生成服务器列表json")
async def make_server_list():
    t1 = time.time()
    print(server_group_name)
    chs = await Channel.all()
    for ch in chs:
        channel_json = {}
        group = await ch.group.all()
        tids = await ch.server.all().annotate().group_by("tabId").values("tabId")
        n = 1
        for tid in tids:
            key = str(tid["tabId"])
            tab_name = server_group_name[key]
            servers = await ch.server.all().filter(tabId=int(key))
            logic = []
            for s in servers:
                logic_server = LogicServer(**s.get_server_json())
                logic_server.ip = s.game_addr
                logic_server.port = int(s.game_port)
                logic_server.createtime = int(time.mktime(s.create_time.timetuple()))
                logic.append(logic_server)
            channel_json[str(n)] = {
                "tabName": tab_name,
                "logic": logic,
            }
            channel_json["version"] = group.version
            channel_json["resource_version"] = group.resource_version
            channel_json["audit_versions"] = group.audit_versions
            channel_json["audit_servers"] = group.audit_servers
            channel_json["cdn"] = group.cdn_url
            channel_json["login"] = group.login_url
            channel_json["card"] = group.card_url
            channel_json["custom"] = group.custom_url
            channel_json["other"] = group.other
            n = n + 1
        await write_json_file(ch.name, channel_json, "server")
        md5_value = await get_md5_file(ch.name)

        md5_json = {}
        md5_json["server"] = md5_value
        md5_json["notice"] = md5_value
        md5_json["version"] = group.version
        md5_json["resource_version"] = group.resource_version
        md5_json["audit_versions"] = group.audit_versions
        md5_json["audit_servers"] = group.audit_servers
        md5_json["cdn"] = group.cdn_url
        md5_json["card"] = group.card_url
        md5_json["custom"] = group.custom_url
        md5_json["other"] = group.other

        print(md5_value)
        await write_json_file(ch.name, md5_json, "md5")
    t2 = time.time()
    t = t2 - t1
    print(f"请求耗时----------{t}")
    return channel_json


async def write_json_file(name, json_data, file_type):
    """
    生成渠道JSON文件
    """
    file_path = os.path.join(settings.STATIC_PATH,f"{file_type}")
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file_name = os.path.join(file_path,f"{name}.json")
    # 同步写入数据
    # with open(file_name, "w", encoding="utf-8") as f:
    #     f.write(json.dumps(jsonable_encoder(channel_json)))

    # 异步写入
    async with aiofiles.open(file_name, "w", encoding="utf-8") as f:
        await f.write(json.dumps(jsonable_encoder(json_data)))


async def get_md5_file(name):
    file_path = os.path.join(settings.STATIC_PATH, "server")
    file_name = os.path.join(file_path, f"{name}.json")
    if not os.path.isfile(file_name):
        return
    hash_data = hashlib.md5()
    async with aiofiles.open(file_name, mode='rb') as f:
        while True:
            byte = await f.read(8096)
            if not byte:
                break
            hash_data.update(byte)
        ret = hash_data.hexdigest()
    return ret

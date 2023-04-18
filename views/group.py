from fastapi import APIRouter, Request, HTTPException, Depends
from models.server import Group
from schemas.group import ResGroups, ResOneGroup, ResGroupChannels, Group_Pydantic, GroupIn_Pydantic
from utils import Response200
from common.logger import logger

group = APIRouter()


@group.post("/", summary="创建一个分区", response_model=Group_Pydantic)
async def create_one_group(g: GroupIn_Pydantic):
    logger.info(f"创建一个服务器-{g.name}")
    ch_obj = await Group.create(**g.dict(exclude_unset=True))
    return Response200(data=ch_obj)


@group.get("/all", summary="获取所有分区", response_model=ResGroups)
async def get_all_group():
    logger.info("获取所有分区")
    all_group = await Group.all()
    return Response200(data=all_group)


@group.get("/{group_id}", summary="获取一个分组信息", response_model=ResOneGroup)
async def get_one_group(group_id: int):
    logger.info(f"获取一个分区信息-{group_id}")
    g = await Group.get(id=group_id)
    return Response200(data=g)


@group.put("/{group_id}", summary="更新一个分区", response_model=ResOneGroup)
async def update_one_group(group_id: int, g: GroupIn_Pydantic):
    logger.info(f"更新一个渠道-{group_id}")
    await Group.filter(id=group_id).update(**g.dict(exclude_unset=True))

    # 返回更新后的模型数据
    data = await Group_Pydantic.from_queryset_single(Group.get(id=group_id))
    return Response200(data=data)


@group.delete("/{group_id}", summary="删除一个分区", response_model=ResOneGroup)
async def delete_one_group(group_id: int):
    logger.info(f"删除一个分区 - {group_id}")
    del_group = await Group.filter(id=group_id)
    if not del_group:
        raise HTTPException(status_code=404, detail=f'Group {group_id} not found')
    else:
        group = del_group[0]
        await group.delete()
    return Response200(data=group)


@group.get("/groups_channels/all", summary="获取所有分区对应的渠道", response_model=ResGroupChannels)
async def get_groups_channels():
    data = {}
    groups = await Group.all()
    print(groups)
    for group in groups:
        print(group)
        data[group.group_key] = await group.channel.all()
        print(data)
    return Response200(data=data)


@group.get("/group_channels/{group_id}", summary="获取单个分区下的渠道", response_model=ResGroupChannels)
async def get_group_channels(group_id: int):
    data = {}
    group = await Group.get(id=group_id)
    data[group.name] = await group.channel.all()
    return Response200(data=data)

from fastapi import APIRouter, Request, HTTPException, Depends
from models.server import Notice
from schemas.notice import ResOneNotice, ResNotices, Notice_Pydantic
from utils import Response200
from common.logger import logger

notice = APIRouter()


@notice.post("/", summary="创建一个公告", response_model=Notice_Pydantic)
async def create_one_group(n: Notice_Pydantic):
    logger.info(f"创建一个服务器-{n.id}")
    notice_obj = await Notice.create(**n.dict(exclude=True))
    return Response200(data=notice_obj)


@notice.get("/all", summary="获取所有公告", response_model=ResNotices)
async def get_all_notice():
    logger.info("获取所有公告")
    all_notice = await Notice.all()
    return Response200(data=all_notice)


@notice.get("/{notice_id}", summary="获取一个公告", response_model=ResOneNotice)
async def get_all_notice(notice_id: int):
    logger.info("获取一个公告")
    n = await Notice.get(id=notice_id)
    return Response200(data=n)


@notice.put("/{notice_id}", summary="更新一个公告", response_model=ResOneNotice)
async def update_one_notice(notice_id: int, n: Notice_Pydantic):
    logger.info(f"更新一个公告-{notice_id}")
    await Notice.filter(id=notice_id).update(**n.dict(exclude=True))

    data = await Notice_Pydantic.from_queryset_single(Notice.get(id=notice_id))
    return Response200(data=data)


@notice.delete("/{notice_id}", summary="删除一个公告", response_model=ResOneNotice)
async def delete_one_notice(notice_id: int):
    logger.info(f"删除一个公告-{notice_id}")
    del_notice = await Notice.filter(id=notice_id)
    if not del_notice:
        raise HTTPException(status_code=404, detail=f"Notice {notice_id} not found")
    else:
        n = del_notice[0]
        await n.delete()
    return Response200(data=n)

from datetime import datetime
from typing import List, Dict
from models.server import Notice
from utils import Response200
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

Notice_Pydantic = pydantic_model_creator(Notice, name="Notice")
Notice_Pydantic_List = pydantic_queryset_creator(Notice, name="NoticeList")
NoticeIn_Pydantic = pydantic_model_creator(Notice, name="NoticeIn", exclude=("id",), exclude_readonly=True)


class ResNotices(Response200):
    data: List[Notice_Pydantic]


class ResOneNotice(Response200):
    data: Notice_Pydantic

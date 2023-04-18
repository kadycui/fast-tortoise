from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from models.server import Server, Channel
from schemas.server import ResServer
from utils import Response200

Channel_Pydantic = pydantic_model_creator(Channel, name="Channel")
Channel_Pydantic_List = pydantic_queryset_creator(Channel, name="ChannelList")
ChannelIn_Pydantic = pydantic_model_creator(Channel, name="ChannelIn", exclude=("id",), exclude_readonly=True)


class ResChannels(Response200):
    data: List[Channel_Pydantic]


class ResOneChannel(Response200):
    data: Channel_Pydantic


class ResChannelServers(Response200):
    data: Dict[str, List[ResServer]]

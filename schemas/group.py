from typing import List, Dict
from models.server import Group
from schemas.channel import Channel_Pydantic
from utils import Response200
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

Group_Pydantic = pydantic_model_creator(Group, name="Group")
Group_Pydantic_List = pydantic_queryset_creator(Group, name="GroupList")
GroupIn_Pydantic = pydantic_model_creator(Group, name="GroupIn", exclude=("id",), exclude_readonly=True)


class ResGroupsChannels(Response200):
    pass


class ResGroups(Response200):
    data: List[Group_Pydantic]


class ResOneGroup(Response200):
    data: Group_Pydantic


class ResGroupChannels(Response200):
    data: Dict[str, List[Channel_Pydantic]]

from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from models.server import Server
from utils import Response200

Server_Pydantic = pydantic_model_creator(Server, name="Server")
ServerIn_Pydantic = pydantic_model_creator(Server, name="ServerIn", exclude=("id",))
Server_Pydantic_List = pydantic_queryset_creator(Server, name="ServerList")


class ResServer(BaseModel):
    id: int
    name: str
    alias: str
    create_time: datetime
    json_data: str
    status: int


class ResServers(Response200):
    data: Dict[str, List[ResServer]]


class ResOneServer(Response200):
    data: Server_Pydantic


class ResQueryServer(Response200):
    data: List[ResServer]

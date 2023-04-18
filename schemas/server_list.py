from datetime import datetime
from pydantic import BaseModel
from typing import List

server_group_name = {"0": "所有服务器", "1": "仙缘服", "2": "奔雷服", "3": "轮回服", "4": "仙梦服", "5": "诛仙服",
                     "6": "魔剑服", "7": "渡情服", "8": "独尊服", "9": "王者服", "10": "青缘服", "11": "白蛇服",
                     "12": "雷劫服", "13": "青蛇服", "14": "渡劫服", "15": "剑冢服", "16": "小青服", "17": "风云服",
                     "18": "仙盟服", "19": "仙境服", "20": "白泽服"}


class LogicServer(BaseModel):
    id: str
    name: str
    ip: str = None
    port: int = None
    status: int
    commend: int
    tabId: int
    master_id: int = 0
    createtime: int = None


class ChannelJson(BaseModel):
    other: str
    version: int
    resource_version: int
    audit_versions: str
    audit_servers: str
    cdn: str
    tabName: str
    login: str
    card: str
    custom: str
    logic: List[LogicServer]

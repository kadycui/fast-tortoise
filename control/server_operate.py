from models.server import Server
from control.base import CRUDBase
from schemas.server import Server_Pydantic


class CURDServer(CRUDBase[Server, Server_Pydantic, Server_Pydantic]):
    async def get_server_by_id(self, pk: int) -> Server:
        return await super().get(pk)

    async def get_server_by_name(self, name: str) -> Server:
        return await self.model.filter(name=name).first()


server_db = CURDServer(Server)

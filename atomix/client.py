from typing import List, Optional
from grpclib.client import Channel
from asyncio import gather
from datetime import timedelta

from .database import AtomixDatabase
from .proto.database import DatabaseId, DatabaseServiceStub

DEFAULT_NAMESPACE = "default"


class AtomixClient:
    def __init__(self, host: str, port: int, namespace: Optional["str"] = DEFAULT_NAMESPACE):
        self.host = host
        self.port = port
        self.namespace = namespace
        self.channel = Channel(host=self.host, port=self.port)

    async def get_database(self, name: str, session_timeout: Optional["timedelta"]) -> AtomixDatabase:
        service = DatabaseServiceStub(self.channel)
        id = DatabaseId(namespace=self.namespace, name=name)
        response = await service.get_database(id=id)
        database = AtomixDatabase(response.database)
        await database.connect(timeout=session_timeout)
        return database

    async def get_databases(self, session_timeout: Optional["int"]) -> List["AtomixDatabase"]:
        service = DatabaseServiceStub(self.channel)
        response = await service.get_databases(namespace=self.namespace)
        databases = list()
        for db in response.databases:
            databases.append(AtomixDatabase(db))
        await gather(*[database.connect(timeout=session_timeout) for database in databases])
        return databases

    def close(self):
        self.channel.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

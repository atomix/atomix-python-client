from asyncio import gather
from datetime import timedelta

from .proto.database import Database
from .session import AtomixSession
from .map import AtomixMap


class AtomixDatabase:
    def __init__(self, database: Database):
        self.database = database
        self.sessions = list()

    async def connect(self, timeout: timedelta):
        self.sessions = list()
        for partition in self.database.partitions:
            self.sessions.append(AtomixSession(partition))
        await gather(*[session.connect(timeout=timeout) for session in self.sessions])

    async def disconnect(self):
        await gather(*[session.disconnect() for session in self.sessions])

    async def get_map(self, name: str) -> AtomixMap:
        return AtomixMap(self.sessions)

    def __exit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

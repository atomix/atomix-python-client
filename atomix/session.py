from typing import Any, Mapping, Optional
from grpclib.client import Channel
from asyncio import sleep

from .proto.database import Partition
from .proto.primitive import PrimitiveId
from .proto.session import *
from .proto.headers import *


class AtomixSession:
    id: int
    channel: Channel
    _last_index: int
    _response_id: int
    _streams: Mapping["int", "int"]

    def __init__(self, partition: Partition):
        self.partition = partition
        self._streams = {}

    def _get_state_header(self, *, primitive: Optional["PrimitiveId"] = None) -> RequestHeader:
        return RequestHeader(
            primitive=primitive,
            partition=self.partition.partition_id.partition,
            index=self._last_index,
            request_id=self._response_id,
            streams=self._get_stream_headers()
        )

    def _get_stream_headers(self) -> List["StreamHeader"]:
        streams = list()
        for id, response in self._streams:
            if id <= self._response_id:
                streams.append(StreamHeader(stream_id=id, response_id=response))
        return streams

    async def connect(self, timeout: timedelta):
        self.channel = Channel(host=self.partition.endpoints[0].host, port=self.partition.endpoints[0].port)
        service = SessionServiceStub(self.channel)
        header = RequestHeader(partition=self.partition.partition_id.partition)
        response = await service.open_session(header=header, timeout=timeout)
        self.id = response.header.session_id
        while True:
            await sleep(timeout.seconds / 2)
            await self.keep_alive()

    async def keep_alive(self):
        header = self._get_state_header()
        response = await self.do_request(header, lambda channel: SessionServiceStub(channel).keep_alive(header=header))

    async def do_session(self, callback: Any):
        service = SessionServiceStub(self.channel)
        header = self._get_state_header()

    async def do_command(self, header: RequestHeader, callback: Any) -> Any:
        pass

    async def do_query(self, header: RequestHeader, callback: Any) -> Any:
        pass

    async def do_request(self, header: RequestHeader, callback: Any) -> Any:
        while True:
            if self.channel is None:
                self.channel = Channel(host=self.partition.endpoints[0].host, port=self.partition.endpoints[0].port)
            try:
                response_header, response = await callback(self.channel)
                if response_header.status == ResponseStatus.OK:
                    self._record_response(header, response_header)
                    return response
                elif response_header.status == ResponseStatus.NOT_LEADER:
                    self.channel = Channel(host=response_header.leader.host, port=response_header.leader.port)
                elif response_header.status == ResponseStatus.ERROR:
                    pass
            except:
                self.channel = None

    async def disconnect(self):
        self.channel.close()

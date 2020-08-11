from typing import List

from .session import AtomixSession


class AtomixMap:
    def __init__(self, partitions: List["AtomixMapPartition"]):
        self.partitions = partitions


class AtomixMapPartition:
    def __init__(self, session: AtomixSession):
        self.session = session

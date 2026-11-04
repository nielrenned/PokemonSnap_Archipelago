import abc
from typing import Sequence
from CommonClient import CommonContext

class PokemonSnapGenericEmuClient(abc.ABC):
    @abc.abstractmethod
    async def read(self, ctx: CommonContext, read_list: Sequence[tuple[int, int, str]]):
        ...

    @abc.abstractmethod
    async def write(self, ctx: CommonContext, write_list: Sequence[tuple[int, Sequence[int], str]]):
        ...
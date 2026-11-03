import abc
from typing import Sequence

class PokemonSnapClient(abc.ABC):
    @abc.abstractmethod
    async def read(read_list: Sequence[tuple[int, int, str]]):
        ...

    @abc.abstractmethod
    async def write(write_list: Sequence[tuple[int, Sequence[int], str]]):
        ...
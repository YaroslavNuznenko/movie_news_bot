from typing import TypedDict
from abc import ABC, abstractmethod


class Location(TypedDict):
    lat: str
    lon: str


class LocationAPI(ABC):
    @abstractmethod
    async def search(self, search_term: str) -> Location:
        pass

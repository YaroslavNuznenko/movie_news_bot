from abc import ABC, abstractmethod

from location import Location


class WeatherForecastAPI(ABC):
    @abstractmethod
    async def get_avg_temperature(self, location: Location, days: int) -> float:
        pass

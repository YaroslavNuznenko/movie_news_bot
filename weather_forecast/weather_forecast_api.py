from abc import ABC, abstractmethod


class WeatherForecastAPI(ABC):
    @abstractmethod
    async def get_avg_temperature(self, location, days) -> float:
        pass

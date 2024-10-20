from abc import ABC, abstractmethod


class WeatherForecastAPI(ABC):
    @abstractmethod
    def get_avg_temperature(self, lat, lon, days):
        pass

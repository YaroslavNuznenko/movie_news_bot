from httpx import AsyncClient

from location import Location

from .weather_forecast_api import WeatherForecastAPI

BASE_URL = "https://api.weatherapi.com/v1/forecast.json"


class WeatherAPI(WeatherForecastAPI):
    # https://www.weatherapi.com/docs/

    def __init__(self, api_key) -> None:
        self.api_key = api_key

    async def get_avg_temperature(self, location: Location, days: int) -> float:
        params = {
            "key": self.api_key,
            "q": f"{location['lat']},{location['lon']}",
            "days": days,
        }

        async with AsyncClient() as client:
            response = await client.get(BASE_URL, params=params)
            data = response.json()

        forecasts = list(
            map(
                lambda f: f["day"]["avgtemp_c"],
                data["forecast"]["forecastday"],
            )
        )

        avg_temp = sum((forecasts)) / len(forecasts)
        return avg_temp

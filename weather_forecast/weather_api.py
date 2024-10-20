import requests

from .weather_forecast_api import WeatherForecastAPI

BASE_URL = "https://api.weatherapi.com/v1/forecast.json"


class WeatherAPI(WeatherForecastAPI):
    # https://www.weatherapi.com/docs/

    def __init__(self, api_key):
        self.api_key = api_key

    def get_avg_temperature(self, lat, lon, days):
        params = {"key": self.api_key, "q": f"{lat},{lon}", "days": days}

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        forecasts = list(
            map(
                lambda f: f["day"]["avgtemp_c"],
                data["forecast"]["forecastday"],
            )
        )

        avg_temp = sum((forecasts)) / len(forecasts)
        return avg_temp

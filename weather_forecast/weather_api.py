import requests

from .weather_forecast_api import WeatherForecastAPI


class WeatherAPI(WeatherForecastAPI):
    # https://www.weatherapi.com/docs/

    def __init__(self, api_key):
        self.api_key = api_key

    def get_api_url(self, lat, lon, days):
        return f"https://api.weatherapi.com/v1/forecast.json?key={self.api_key}&q={lat},{lon}&days={days}"  # noqa

    def get_avg_temperature(self, lat, lon, days):
        response = requests.get(self.get_api_url(lat, lon, days))
        data = response.json()

        forecasts = list(
            map(
                lambda f: f["day"]["avgtemp_c"],
                data["forecast"]["forecastday"],
            )
        )

        avg_temp = sum((forecasts)) / len(forecasts)
        return avg_temp

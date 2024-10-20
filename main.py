import os

from dotenv import load_dotenv

from geolocation import nominatim_search_geolocation
from weather_forecast import WeatherAPI


def main():
    load_dotenv()

    city = "Київ"
    location = nominatim_search_geolocation(city)

    if location is None or "lat" not in location or "lon" not in location:
        print(f"Could not find location for the {city}")
        return

    weather_api_key = os.getenv("WEATHER_API_KEY")
    weather_api = WeatherAPI(weather_api_key)

    days = 7
    avg_temp = weather_api.get_avg_temperature(**location, days=days)
    print(f"Avg temperature in {city} for the next {days} days is {avg_temp}°C")  # noqa


if __name__ == "__main__":
    main()

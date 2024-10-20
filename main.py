import os

from dotenv import load_dotenv

from weather_forecast import WeatherAPI


def main():
    load_dotenv()

    weather_api_key = os.getenv("WEATHER_API_KEY")
    weather_api = WeatherAPI(weather_api_key)

    lat = 51.5074
    lon = 0.1278
    days = 7

    avg_temp = weather_api.get_avg_temperature(lat, lon, days)
    print(f"Avg temperature for the next {days} days is {avg_temp}°C")


if __name__ == "__main__":
    main()

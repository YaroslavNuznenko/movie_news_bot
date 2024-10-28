import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from chat import settings_router
from location import NominatimAPI
from weather_forecast import WeatherAPI

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    location_api = NominatimAPI()
    weather_forecast_api = WeatherAPI(WEATHER_API_KEY)

    dp = Dispatcher(location_api=location_api, weather_forecast_api=weather_forecast_api)
    dp.include_router(settings_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

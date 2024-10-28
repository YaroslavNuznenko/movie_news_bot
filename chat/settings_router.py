from typing import Dict

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from location import LocationAPI
from weather_forecast import WeatherForecastAPI

settings_router = Router()


class Settings(StatesGroup):
    location = State()
    coordinates_location = State()
    place_location = State()


class LocationSettingType:
    Coordinates = "coordinates"
    Place = "place"


@settings_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    # TODO: check if the user already has location set
    await state.set_state(Settings.location)
    await message.answer(
        "\n".join(
            [
                "Hello!",
                "Please, select the way how you want to set your location:",
                " - Coordinates - latitude and longitude;",
                " - Place - settlement name.",
            ]
        ),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=LocationSettingType.Coordinates.capitalize()),
                    KeyboardButton(text=LocationSettingType.Place.capitalize()),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@settings_router.message(Settings.location, F.text.casefold() == LocationSettingType.Place)
async def process_location_with_place(message: Message, state: FSMContext) -> None:
    await state.set_state(Settings.place_location)
    await message.answer(
        "Enter the name of the settlement",
        reply_markup=ReplyKeyboardRemove(),
    )


@settings_router.message(Settings.place_location)
async def process_place_location(
    message: Message, state: FSMContext, location_api: LocationAPI, weather_forecast_api: WeatherForecastAPI
) -> None:
    q = message.text.strip()

    location = await location_api.search(q)

    if location is None:
        await message.answer("Location not found, please, try again.")
        return

    await state.clear()

    await show_avg_temperature(message, weather_forecast_api, {"location": location})


async def show_avg_temperature(message: Message, weather_forecast_api: WeatherForecastAPI, data=Dict[str, any]) -> None:
    days = 7
    location = data["location"]

    avg_temperature = await weather_forecast_api.get_avg_temperature(location, days)

    await message.answer(
        f"Average temperature for the next {days} days: {avg_temperature:.1f}°C", reply_markup=ReplyKeyboardRemove()
    )

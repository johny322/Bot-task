# роутер для работы с погодой
from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot import texts
from tgbot.misc.states import WeatherStatesGroup
from tgbot.services.weather.api import WeatherApi

weather_router = Router()


@weather_router.message(commands='weather')
async def weather_handler(message: types.Message, state: FSMContext):
    await message.answer(
        texts.start_weather_text
    )
    await state.set_state(WeatherStatesGroup.city)


@weather_router.message(WeatherStatesGroup.city)
async def weather_handler(message: types.Message, state: FSMContext, weather_api: WeatherApi):
    # weather_api прилетело из мидлваря
    city_name = message.text
    text = await weather_api.get_weather(city_name)
    if not text:
        await message.answer(texts.bad_weather_text.format(city_name=city_name))
    else:
        await message.answer(text)
    await state.clear()

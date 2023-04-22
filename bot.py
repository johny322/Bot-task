import asyncio
import logging
from typing import List

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.handlers.admin import admin_router
from tgbot.handlers.users import user_router
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.objects import GetObjectsMiddleware
from tgbot.misc.bot_commands import set_bot_commands
from tgbot.services import broadcaster
from tgbot.services.currency.api import CurrencyApi
from tgbot.services.random_photo.api import RandomPhoto
from tgbot.services.weather.api import WeatherApi

config = load_config(".env")


def setup_logger():
    """
    установка логгера
    :return:
    """
    logger = logging.getLogger('main_logger')
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    strfmt = "[%(asctime)s] [%(levelname)-8s] --- %(message)s (%(filename)s:%(funcName)s:%(lineno)s)"

    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(strfmt, datefmt)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.info('Set up logger')

    return logger


logger = setup_logger()


async def on_startup(bot: Bot, admin_ids: List[int]):
    await set_bot_commands(bot, admin_ids)  # установка команд бота
    await broadcaster.broadcast(bot, admin_ids, "Бот был запущен")  # рассылка админам при старте бота


async def on_shutdown(random_photo_api: RandomPhoto, currency_api: CurrencyApi, weather_api: WeatherApi):
    # закрытие сессий aiohttp
    await random_photo_api.close()
    await currency_api.close()
    await weather_api.close()


def register_global_middlewares(dp: Dispatcher, config, bot, logger, **kwargs):
    """
    регистрация мидлварей
    :param dp:
    :param config:
    :param bot:
    :param logger:
    :param kwargs:
    :return:
    """
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))

    dp.message.middleware(GetObjectsMiddleware(logger=logger, bot=bot, config=config, **kwargs))
    dp.callback_query.middleware(GetObjectsMiddleware(logger=logger, bot=bot, config=config, **kwargs))


async def main():
    logger.info("Starting bot")

    # установка хранилища для машины состояний
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    # регистрация роутеров(хендлеров)
    for router in [
        admin_router,
        user_router,
    ]:
        dp.include_router(router)

    # объекты для работы с api фото, валюты и погоды
    random_photo_api = RandomPhoto()
    currency_api = CurrencyApi(config.api_keys.currency)
    weather_api = WeatherApi(config.api_keys.weather)

    # передаем объекты в мидлвари для возможности использования их в хендлерах
    register_global_middlewares(
        dp, config, logger=logger, bot=bot,
        random_photo_api=random_photo_api,
        currency_api=currency_api,
        weather_api=weather_api,
    )

    await on_startup(bot, config.tg_bot.admin_ids)
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown(
            random_photo_api=random_photo_api,
            currency_api=currency_api,
            weather_api=weather_api,
        )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот был выключен!")

import asyncio
import datetime
import logging
from typing import Optional

import aiohttp

logger = logging.getLogger('main_logger')


class WeatherApi:
    def __init__(self, api_token: str):
        self.__api_token = api_token
        self._session = None

    async def get_session(self) -> aiohttp.ClientSession:
        """
        создание сессии aiohttp
        сессия создается только один раз и используется  в последующих запросах
        :return:
        """
        if self._session is None:
            new_session = aiohttp.ClientSession()
            self._session = new_session
        return self._session

    async def close(self) -> None:
        """
        закрытие сессии
        :return:
        """
        if self._session is None:
            return None
        await self._session.close()

    async def get_weather(self, city_name: str) -> Optional[str]:
        """
        получение данных о погоде
        в результате сразу возвращается отформатированный текст с даннфми о погоде
        :param city_name:
        :return:
        """
        api_url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.__api_token}&units=metric'
        session = await self.get_session()
        try:
            res = await session.get(api_url)
            data = await res.json()
        except Exception:
            logger.exception('Ошибка при попытке получить данные о погоде')
            return
        try:
            weather_text = self.process_weather_data(data)
        except Exception:
            logger.exception('Ошибка при попытке парсинга данных погоды')
            weather_text = None
        return weather_text

    def process_weather_data(self, data: dict) -> Optional[str]:
        """
        плучение данных из json
        :param data:
        :return:
        """
        if not data:
            return
        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Ясно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Мелкий дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }
        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Состояние погоды неизвестно'
        humidity = data['main']["humidity"]
        pressure = data['main']['pressure']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - \
                            datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        wind = data['wind']['speed']
        text = f'***{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}***\n' \
               f'Погода в городе: {city}\n' \
               f'Температура: {cur_weather}C° {wd}\n' \
               f'Влажность: {humidity}%\n' \
               f'Давление: {pressure} мм.рт.ст\n' \
               f'Ветер: {wind} м/c\n' \
               f'Восход солнца: {sunrise_timestamp}\n' \
               f'Закат солнца: {sunset_timestamp}\n' \
               f'Продолжительность дня: {length_of_the_day}\n' \
               f'Хорошего дня!'
        return text


async def test():
    name = 'moscow'
    weather_api = WeatherApi('')
    print(await weather_api.get_weather(name))


if __name__ == '__main__':
    asyncio.run(test())

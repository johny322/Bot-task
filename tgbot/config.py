from dataclasses import dataclass
from typing import List

from environs import Env


@dataclass
class TgBot:
    token: str
    bot_username: str
    admin_ids: List[int]
    admin_username: str

    def bot_link(self):
        return f'https://t.me/{self.bot_username}'


@dataclass
class ApiKeys:
    weather: str
    currency: str


@dataclass
class Config:
    tg_bot: TgBot
    api_keys: ApiKeys


def load_config(path: str = None):
    """
    функция для получения данных из переменных окружения, которые загружаются из файла .env
    для хранения данных используются датаклассы
    :param path:
    :return:
    """
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            bot_username=env.str("BOT_USERNAME"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            admin_username=env.str('ADMIN_USERNAME')
        ),
        api_keys=ApiKeys(
            weather=env.str("WEATHER_API"),
            currency=env.str("CURRENCY_API"),
        ),
    )

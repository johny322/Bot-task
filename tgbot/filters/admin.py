from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message

from tgbot.config import Config


class AdminFilter(BaseFilter):
    """
    фильтр для админа
    """
    is_admin: bool = True

    async def __call__(self, obj: Message, config: Config) -> bool:
        # проверка есть ли id пользователя, который написал боту в списке админов из конфига
        return (obj.from_user.id in config.tg_bot.admin_ids) == self.is_admin

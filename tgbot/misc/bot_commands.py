from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat


async def set_bot_commands(bot: Bot, admin_ids):
    """
    Установка команд в бота
    :param bot:
    :param admin_ids:
    :return:
    """
    await bot.set_my_commands(
        commands=[
            BotCommand(
                command='start',
                description='🤖 Перезапустить бота'
            ),
            BotCommand(
                command='weather',
                description='Узнать погоду'
            ),
            BotCommand(
                command='currency',
                description='Конвертация валюты'
            ),
            BotCommand(
                command='cat',
                description='Случайное фото котика'
            ),
            BotCommand(
                command='poll',
                description='Отправка опроса в группу'
            ),
            BotCommand(
                command='cancel',
                description='Отмена действия'
            ),

        ]
    )

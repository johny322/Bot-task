# файл с текстовыми клавиатурами
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.texts import keyboard_texts

cancel_button = KeyboardButton(text=keyboard_texts.btn_cancel)

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=keyboard_texts.btn_start_menu)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)

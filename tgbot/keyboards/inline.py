# файл с инлайн клавиатурами
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.texts import keyboard_texts


def yes_no_inline_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=keyboard_texts.btn_yes,
            callback_data='yes'
        ),
        InlineKeyboardButton(
            text=keyboard_texts.btn_no,
            callback_data='no'
        ),

    )
    return builder.as_markup()

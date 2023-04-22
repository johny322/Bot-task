# роутер на команду start
from aiogram import Router
from aiogram.dispatcher.filters import CommandObject
from aiogram.dispatcher.filters.command import CommandStart
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message

from tgbot import texts
from tgbot.keyboards.reply import start_keyboard
from tgbot.texts import keyboard_texts

user_router = Router()


@user_router.message(CommandStart())
async def user_start_handler(message: Message, state: FSMContext, command: CommandObject):
    await state.clear()
    text = f"{texts.start_user_message_text}\n" \
           f"{texts.menu_text}"

    await message.answer(
        text=text,
        reply_markup=start_keyboard
    )


@user_router.message(text=keyboard_texts.btn_start_menu)
async def user_start_handler(message: Message, state: FSMContext):
    await message.answer(
        text=texts.menu_text,
        reply_markup=start_keyboard
    )

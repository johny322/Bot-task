# роутер админа
from aiogram import Router, types
from aiogram.dispatcher.filters import CommandObject
from aiogram.dispatcher.filters.command import CommandStart
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot import texts
from tgbot.filters.admin import AdminFilter
from tgbot.keyboards.reply import start_keyboard

admin_router = Router()
# задание фильтра на роутер под id админа
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart(), state="*")
async def admin_start(message: types.Message, state: FSMContext, command: CommandObject):
    await state.clear()
    text = f"{texts.start_admin_message_text}\n" \
           f"{texts.menu_text}"

    await message.answer(
        text=text,
        reply_markup=start_keyboard
    )

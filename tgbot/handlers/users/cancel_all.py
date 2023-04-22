# роутер для отмены действий
from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot import texts
from tgbot.keyboards.reply import start_keyboard

cancel_router = Router()


@cancel_router.callback_query(text='cancel', state='*')
async def cancel_all_handler(query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.delete()
    await query.message.answer(
        text=texts.success_cancel_text,
        reply_markup=start_keyboard
    )


@cancel_router.message(commands='cancel', state='*')
async def cancel_all_command_handler(query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.delete()
    await query.message.answer(
        text=texts.success_cancel_text,
        reply_markup=start_keyboard
    )

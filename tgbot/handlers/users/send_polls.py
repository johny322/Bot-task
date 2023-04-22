# роутер на создание опросов
from aiogram import Router, types, Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from tgbot import texts
from tgbot.keyboards.inline import yes_no_inline_keyboard
from tgbot.misc.states import PollStatesGroup
from tgbot.texts import keyboard_texts

poll_router = Router()


@poll_router.message(commands='poll')
async def make_poll_handler(message: types.Message, state: FSMContext):
    await message.answer(texts.make_poll_title_text)
    await state.set_state(PollStatesGroup.title)


@poll_router.message(PollStatesGroup.title)
async def poll_answers_handler(message: types.Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)
    await message.answer(texts.make_poll_answers_text)
    await state.set_state(PollStatesGroup.answers)


@poll_router.message(PollStatesGroup.answers)
async def poll_chat_id_handler(message: types.Message, state: FSMContext):
    answers = message.text.split('\n')
    await state.update_data(answers=answers)
    await message.answer(texts.make_poll_chat_id_text)
    await state.set_state(PollStatesGroup.chat_id)


@poll_router.message(PollStatesGroup.chat_id)
async def poll_confirm_handler(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    title = data['title']
    answers = data['answers']

    chat_id = message.text
    try:
        await message.answer_poll(
            question=title,
            options=answers
        )
    except Exception:
        await message.answer(texts.bad_make_poll_text)
        await state.clear()
        return
    try:
        member = await bot.get_chat_member(chat_id, bot.id)
    except TelegramBadRequest as e:
        await message.answer(texts.make_poll_chat_id_error_text.format(chat_id=chat_id))
        return

    await state.update_data(chat_id=chat_id)
    await message.answer(
        texts.make_poll_confirm_text.format(chat_id=chat_id),
        reply_markup=yes_no_inline_keyboard()
    )
    await state.set_state(PollStatesGroup.confirm)


@poll_router.callback_query(text='yes', state=PollStatesGroup.confirm)
async def send_poll_handler(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    title = data['title']
    answers = data['answers']
    chat_id = data['chat_id']

    await state.clear()
    try:
        await bot.send_poll(
            chat_id=chat_id,
            question=title,
            options=answers
        )
        await call.message.edit_text(text=texts.good_send_poll_text)
    except Exception:
        await call.message.edit_text(text=texts.bad_send_poll_text)
    finally:
        await call.answer()


@poll_router.callback_query(text='no', state=PollStatesGroup.confirm)
async def no_send_poll_handler(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()
    await call.message.edit_text(text=texts.success_cancel_text)
    await call.answer()

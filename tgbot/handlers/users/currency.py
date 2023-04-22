# роутер для работы с валютами
from aiogram import Router, types
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot import texts
from tgbot.misc.states import CurrencyStatesGroup
from tgbot.services.currency.api import CurrencyApi

currency_router = Router()


@currency_router.message(commands='currency_symbols')
async def currency_symbols_handler(message: types.Message, currency_api: CurrencyApi):
    symbols_text = await currency_api.get_symbols()
    if symbols_text:
        await message.answer(symbols_text)
    else:
        await message.answer(texts.bad_currency_text)


@currency_router.message(commands='currency')
async def currency_handler(message: types.Message, state: FSMContext, currency_api: CurrencyApi):
    await message.answer(texts.from_currency_text)
    await state.set_state(CurrencyStatesGroup.from_currency)


@currency_router.message(CurrencyStatesGroup.from_currency)
async def from_currency_handler(message: types.Message, state: FSMContext, currency_api: CurrencyApi):
    from_currency = message.text
    await state.update_data(from_currency=from_currency)
    await message.answer(texts.to_currency_text)
    await state.set_state(CurrencyStatesGroup.to_currency)


@currency_router.message(CurrencyStatesGroup.to_currency)
async def to_currency_handler(message: types.Message, state: FSMContext, currency_api: CurrencyApi):
    data = await state.get_data()
    from_currency = data['from_currency']
    to_currency = message.text
    await state.update_data(to_currency=to_currency)
    await message.answer(texts.amount_currency_text.format(
        from_currency=from_currency,
        to_currency=to_currency
    ))
    await state.set_state(CurrencyStatesGroup.amount)


@currency_router.message(CurrencyStatesGroup.amount)
async def amount_currency_handler(message: types.Message, state: FSMContext, currency_api: CurrencyApi):
    amount = message.text
    try:
        amount = float(amount.replace(',', '.'))
    except ValueError:
        await message.answer(texts.bad_amount_currency_text)
        return
    data = await state.get_data()
    from_currency = data['from_currency']
    to_currency = data['to_currency']

    res_amount = await currency_api.convert_currency(from_currency, to_currency, amount)
    if res_amount:
        text = texts.result_currency_text.format(
            amount=amount,
            from_currency=from_currency,
            to_currency=to_currency,
            res_amount=res_amount
        )
    else:
        text = texts.bad_currency_text
    await message.answer(text)
    await state.clear()

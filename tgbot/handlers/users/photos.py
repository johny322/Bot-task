# роутер на отправку фото
from aiogram import Router, types

from tgbot import texts
from tgbot.services.random_photo.api import RandomPhoto

router = Router()


@router.message(commands='cat')
async def send_cat_handler(message: types.Message, random_photo_api: RandomPhoto):
    url = await random_photo_api.get_random_photo()
    if url:
        await message.answer_photo(
            photo=url
        )
    else:
        await message.answer(texts.bad_photo_text)

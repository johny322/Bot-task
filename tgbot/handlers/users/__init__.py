from aiogram import Router

from .cancel_all import cancel_router
from .start import user_router as start_router
from .photos import router as photo_router
from .send_polls import poll_router
from .weather import weather_router
from .currency import currency_router

user_router = Router()
user_router.include_router(start_router)
user_router.include_router(cancel_router)
user_router.include_router(photo_router)
user_router.include_router(poll_router)
user_router.include_router(weather_router)
user_router.include_router(currency_router)

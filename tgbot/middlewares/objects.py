from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class GetObjectsMiddleware(BaseMiddleware):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        for key, value in self.kwargs.items():
            data[key] = value
        return await handler(event, data)

import asyncio
import logging
from typing import Optional

import aiohttp

logger = logging.getLogger('main_logger')


class RandomPhoto:
    def __init__(self):
        self._session = None

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            new_session = aiohttp.ClientSession()
            self._session = new_session
        return self._session

    async def close(self) -> None:
        if self._session is None:
            return None
        await self._session.close()

    async def get_random_photo(self) -> Optional[str]:
        session = await self.get_session()
        url = 'https://api.thecatapi.com/v1/images/search'
        try:
            res = await session.get(url)
            data = await res.json()
        except Exception:
            logger.exception('Ошибка при попытке получения данных о случайной картинке')
            return
        try:
            return data[0]['url']
        except Exception:
            logger.exception('Ошибка при попытке получения ссылки на картинку')


async def test():
    rp = RandomPhoto('dsa')
    res = await rp.get_random_photo()
    print(res)
    await rp.close()


if __name__ == '__main__':
    asyncio.run(test())

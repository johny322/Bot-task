import asyncio
import logging
from typing import Optional, Union

import aiohttp

logger = logging.getLogger('main_logger')


class CurrencyApi:
    def __init__(self, api_token: str):
        self.__api_token = api_token
        self._headers = {
            "apikey": self.__api_token
        }
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

    async def convert_currency(self, from_currency: str, to_currency: str, amount: Union[str, float]) -> Optional[int]:
        url = f'https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}'
        session = await self.get_session()
        try:
            res = await session.get(
                url,
                headers=self._headers,
                timeout=2
            )
            data = await res.json()
        except Exception:
            logger.exception('Ошибка при попытке конвертации валюты')
            return
        return data.get('result')

    def _process_convert_currency(self, data: dict):

        pass

    async def get_symbols(self) -> Optional[str]:
        url = "https://api.apilayer.com/exchangerates_data/symbols"
        session = await self.get_session()
        try:
            res = await session.get(
                url,
                headers=self._headers
            )
            data = await res.json()
        except Exception:
            logger.exception('Ошибка при попытке получения данных о валютах')
            return
        try:
            return self._process_symbols(data)
        except Exception:
            logger.exception('Ошибка при обработке данных о валюте')

    def _process_symbols(self, data: dict) -> str:
        symbols: dict = data['symbols']
        return '\n'.join([f'{key}: {value}' for key, value in symbols.items()])


async def test():
    token = ''
    currency_api = CurrencyApi(token)
    from_currency = 'rub'
    to_currency = 'usd'
    amount = 1000
    print(
        await currency_api.convert_currency(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount
        )
    )
    # print(await currency_api.get_symbols())

    await currency_api.close()


if __name__ == '__main__':
    asyncio.run(test())

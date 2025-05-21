import os
from typing import List

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from schemas import CurrencyRate
from service import get_cny_price, get_usd_price
app = FastAPI()

@app.on_event("startup")
async def startup():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_client = redis.from_url(redis_url)
    FastAPICache.init(RedisBackend(redis_client), prefix="exchange-cache")

@app.get("/currency", response_model=List[CurrencyRate])
@cache(expire=60)  # кэш на 60 секунд
async def get_currency():
    print("🔄 Выполняется парсинг и возврат данных")
    cny_rub = await get_cny_price()
    cny_usd = await get_usd_price()

    cny_rub_cash = cny_rub  * 1.004
    cny_rub_card = cny_rub  * 1.005

    cny_usd_card = cny_usd_cash = cny_usd * 0.975

    return [
        CurrencyRate(pair="CNY/RUB", rate=cny_rub_card, type="Card"),
        CurrencyRate(pair="CNY/RUB", rate=cny_rub_cash, type="Cash"),
        CurrencyRate(pair="CNY/USD", rate=cny_usd_card, type="Card"),
        CurrencyRate(pair="CNY/USD", rate=cny_usd_cash, type="Cash"),
    ]


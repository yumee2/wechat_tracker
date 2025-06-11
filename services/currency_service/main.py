import json
import os
from typing import List, Dict

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from pydantic import BaseModel

from schemas import CurrencyRate
from service import get_cny_price, get_usd_price
app = FastAPI()
redis_client = None

class Multipliers(BaseModel):
    data: Dict[str, Dict[str, float]]

@app.on_event("startup")
async def startup():
    global redis_client
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis_client = redis.from_url(redis_url)
    FastAPICache.init(RedisBackend(redis_client), prefix="exchange-cache")

@app.get("/multipliers", response_model=Multipliers)
async def get_multipliers():
    data = await redis_client.hgetall("exchange-multipliers")
    if not data:
        raise HTTPException(status_code=404, detail="No multipliers found")
    multipliers = {pair: json.loads(rate_dict) for pair, rate_dict in data.items()}
    return {"data": multipliers}

@app.post("/multipliers")
async def set_multipliers(multipliers: Multipliers):
    try:
        for pair, rate_dict in multipliers.data.items():
            # Сохраняем как JSON
            await redis_client.hset("exchange-multipliers", pair, json.dumps(rate_dict))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/currency", response_model=List[CurrencyRate])
@cache(expire=60)  # кэш на 60 секунд
async def get_currency():
    print("🔄 Выполняется парсинг и возврат данных")
    cny_rub = await get_cny_price()
    cny_usd = await get_usd_price()

    raw = await redis_client.hgetall("exchange-multipliers")
    if not raw:
        raise HTTPException(status_code=500, detail="Коэффициенты не заданы")

    try:
        multipliers: Dict[str, Dict[str, float]] = {}
        for key_bytes, json_bytes in raw.items():
            key = key_bytes.decode("utf-8")
            multipliers[key] = json.loads(json_bytes)  # JSON из bytes тоже поймёт
        return [
            CurrencyRate(pair="CNY/RUB", rate=cny_rub * multipliers["CNY/RUB"]["Card"], type="Card"),
            CurrencyRate(pair="CNY/RUB", rate=cny_rub * multipliers["CNY/RUB"]["Cash"], type="Cash"),
            CurrencyRate(pair="CNY/USD", rate=cny_usd * multipliers["CNY/USD"]["Card"], type="Card"),
            CurrencyRate(pair="CNY/USD", rate=cny_usd * multipliers["CNY/USD"]["Cash"], type="Cash"),
        ]
    except (KeyError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail=f"Ошибка в структуре коэффициентов: {e}")
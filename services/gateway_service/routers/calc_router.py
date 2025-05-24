from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from routers.currency_router import get_currency
import httpx
import json

from save_to_telegram import send_message_to_telegram


class CalcRequest(BaseModel):
    weight: float
    volume: float
    cargo_type: str
    user_id: str
    user_name:str



CALC_SERVICE_URL = "http://calc-service:8004"

router = APIRouter()

@router.get("/price_table", summary="Get price table")
async def get_price_table():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{CALC_SERVICE_URL}/calc/price_table")
    return JSONResponse(content=resp.json(), status_code=resp.status_code)

@router.post("/calculate", summary="Calculate price")
async def calculate_price(data: CalcRequest):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{CALC_SERVICE_URL}/calculate", json=data.dict())
        json_data = resp.json()
        currencies_data = await get_currency()
        currencies = json.loads(currencies_data.body.decode('utf-8'))
        yuan_rub = round(currencies[0]["rate"], 3)
        yuan_usd = round(currencies[2]["rate"], 3)
        send_message_to_telegram({
            "yuan_rub": yuan_rub,
            "yuan_usd": yuan_usd,
            "user_name": data.user_name,
            "user_link": f"tg://user?id={data.user_id}",
            "density": json_data.get("density"),
            "total_price": json_data.get("total_price"),
            "cargo_type": "хозтовары" if json_data.get("cargo_type") == "household" else "другое"
        })
        return JSONResponse(content=resp.json(), status_code=resp.status_code)


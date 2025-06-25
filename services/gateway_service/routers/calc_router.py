from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import httpx

from save_to_telegram import send_message_to_telegram


class CalcRequest(BaseModel):
    weight: float
    volume: float
    cargo_type: str
    user_id: str
    user_name:str
    boxes_amount: int


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
        if (data.weight > 50 or data.boxes_amount > 20):
            send_message_to_telegram({
                "user_name": data.user_name,
                "user_link": f"tg://user?id={data.user_id}",
                "density": data.weight / data.volume,
                "total_price": json_data,
                "cargo_type": "хозтовары" if data.cargo_type == "household" else "другое",
                "weight": data.weight,
                "boxes_amount": data.boxes_amount
            })
        else:
            send_message_to_telegram({
                "user_name": data.user_name,
                "user_link": f"tg://user?id={data.user_id}",
                "density": data.weight / data.volume,
                "total_price": json_data,
                "cargo_type": "хозтовары" if data.cargo_type == "household" else "другое",
                "weight": data.weight,
                "boxes_amount": None

            })
        return JSONResponse(content=resp.json(), status_code=resp.status_code)


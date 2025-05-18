from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import httpx

class CalcRequest(BaseModel):
    weight: float
    volume: float
    cargo_type: str


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
    return JSONResponse(content=resp.json(), status_code=resp.status_code)


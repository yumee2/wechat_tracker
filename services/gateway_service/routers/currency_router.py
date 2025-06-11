from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
import httpx


CURRENCY_SERVICE_URL = "http://currency-service:8003"

router = APIRouter()

@router.get("", summary="Get currencies data")
async def get_currency():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{CURRENCY_SERVICE_URL}/currency")
    return JSONResponse(content=resp.json(), status_code=resp.status_code)

@router.get("/multipliers", summary="Get current exchange multipliers")
async def get_multipliers():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{CURRENCY_SERVICE_URL}/multipliers")
    return JSONResponse(content=resp.json(), status_code=resp.status_code)

@router.post("/multipliers", summary="Update exchange multipliers")
async def update_multipliers(payload: dict = Body(...)):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{CURRENCY_SERVICE_URL}/multipliers", json=payload)
    return JSONResponse(content=resp.json(), status_code=resp.status_code)

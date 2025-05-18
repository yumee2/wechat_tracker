from fastapi import APIRouter
from fastapi.responses import JSONResponse
import httpx

CURRENCY_SERVICE_URL = "http://currency-service:8003"

router = APIRouter()

@router.get("/", summary="Get currencies data")
async def get_currency():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{CURRENCY_SERVICE_URL}/currency")
    return JSONResponse(content=resp.json(), status_code=resp.status_code)
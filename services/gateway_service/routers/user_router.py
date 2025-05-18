from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import httpx

USER_SERVICE_URL = "http://users-service:8001"

router = APIRouter()

class UserCreate(BaseModel):
    telegram_id: str
    username: str
    first_name: str


@router.post("/auth/verify", summary="Create user")
async def get_currency(user: UserCreate):
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{USER_SERVICE_URL}/auth/verify", json=user.dict())
    return JSONResponse(content=resp.json(), status_code=resp.status_code)

@router.post("/auth/me/{telegram_id}", summary="Authorization")
async def get_currency(telegram_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{USER_SERVICE_URL}/auth/me/{telegram_id}")
    return JSONResponse(content=resp.json(), status_code=resp.status_code)
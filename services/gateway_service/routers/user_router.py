from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from httpx import Timeout
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

@router.get("/{user_id}/order/{order_no}")
async def get_order_info(order_no: str, user_id: str):
    timeout = Timeout(20.0)  # 10 seconds timeout for the request
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            resp = await client.get(f"{USER_SERVICE_URL}/{user_id}/order/{order_no}")
            resp.raise_for_status()  # Raises an exception for 4XX/5XX responses
            return JSONResponse(content=resp.json(), status_code=resp.status_code)
        except httpx.HTTPStatusError as e:
            # Handle 4XX/5XX responses from the microservice
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Microservice error: {e.response.text}"
            )
        except httpx.RequestError as e:
            # Handle connection errors, timeouts, etc.
            raise HTTPException(
                status_code=503,
                detail=f"Service unavailable: {str(e)}"
            )
        except Exception as e:
            # Handle any other unexpected errors
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )
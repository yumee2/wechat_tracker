from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import init_db, get_db
from models import User
from schemas import UserCreate, UserResponse

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()


@app.post("/auth/verify", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.telegram_id == user.telegram_id)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(status_code=409, detail="user already exists")

    new_user = User(
        telegram_id=user.telegram_id,
        first_name=user.first_name,
        username=user.username,
        is_admin=False,
    )

    db.add(new_user)
    await db.commit()

    return UserResponse(
        id=new_user.id,
        telegram_id=new_user.telegram_id,
        username=new_user.username,
        first_name=new_user.first_name,
        is_admin=new_user.is_admin,
    )

@app.get("/auth/me/{telegram_id}", response_model=UserResponse)
async def get_user(telegram_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    else:
        return UserResponse(
            id=existing_user.id,
            telegram_id=existing_user.telegram_id,
            username=existing_user.username,
            first_name=existing_user.first_name,
            is_admin=existing_user.is_admin,
        )

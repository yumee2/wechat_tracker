from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import init_db, get_db
from models import User, Tracker
from schemas import UserCreate, UserResponse
import requests
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

@app.get("/{user_id}/order/{order_no}")
async def get_order_info(order_no: str, user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Tracker).where(Tracker.tracking_code == order_no)
    )
    tracker = result.scalar_one_or_none()

    if tracker is None:
        response = requests.post("http://147.45.147.92:1241/track", json={"track": order_no})
        print(response.json())
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=response.text)
        else:
            tracker = response.json().get("info")
            state_1 = None
            state_2 = None
            state_3 = None
            state_4 = None
            state_5 = None
            state_6 = None

            if len(tracker.get("tracking")) == 1:
                state_1 = tracker.get("tracking")[0].get("details")
            if len(tracker.get("tracking")) == 2:
                state_1 = tracker.get("tracking")[1].get("details")
                state_2 = tracker.get("tracking")[0].get("details")
            if len(tracker.get("tracking")) == 3:
                state_1 = tracker.get("tracking")[2].get("details")
                state_2 = tracker.get("tracking")[1].get("details")
                state_3 = tracker.get("tracking")[0].get("details")
            if len(tracker.get("tracking")) == 4:
                state_1 = tracker.get("tracking")[3].get("details")
                state_2 = tracker.get("tracking")[2].get("details")
                state_3 = tracker.get("tracking")[1].get("details")
                state_4 = tracker.get("tracking")[0].get("details")
            if len(tracker.get("tracking")) == 5:
                state_1 = tracker.get("tracking")[4].get("details")
                state_2 = tracker.get("tracking")[3].get("details")
                state_3 = tracker.get("tracking")[2].get("details")
                state_4 = tracker.get("tracking")[1].get("details")
                state_5 = tracker.get("tracking")[0].get("details")
            if len(tracker.get("tracking")) == 6:
                state_1 = tracker.get("tracking")[5].get("details")
                state_2 = tracker.get("tracking")[4].get("details")
                state_3 = tracker.get("tracking")[3].get("details")
                state_4 = tracker.get("tracking")[2].get("details")
                state_5 = tracker.get("tracking")[1].get("details")
                state_6 = tracker.get("tracking")[0].get("details")

            new_tracker = Tracker(
                tracking_code=order_no,
                user_id=user_id,
                state_1=state_1,
                state_2=state_2,
                state_3=state_3,
                state_4=state_4,
                state_5=state_5,
                state_6=state_6,
            )

            db.add(new_tracker)
            await db.commit()
            return {"state": new_tracker.most_recent_state()}

    else:
        return {"state": tracker.most_recent_state()}

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
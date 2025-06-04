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

        tracker_info = response.json().get("info")
        tracking_events = tracker_info.get("tracking", [])

        # Build state list from latest to oldest, up to 6 entries
        states = []
        for event in reversed(tracking_events[:6]):
            states.append({
                "details": event.get("details"),
                "date": event.get("date")
            })

        # Pad with None if fewer than 6 states
        while len(states) < 6:
            states.append(None)

        new_tracker = Tracker(
            tracking_code=order_no,
            user_id=user_id,
            state_1=states[0],
            state_2=states[1],
            state_3=states[2],
            state_4=states[3],
            state_5=states[4],
            state_6=states[5],
        )

        db.add(new_tracker)
        await db.commit()

        return {
            "state_1": new_tracker.state_1,
            "state_2": new_tracker.state_2,
            "state_3": new_tracker.state_3,
            "state_4": new_tracker.state_4,
            "state_5": new_tracker.state_5,
            "state_6": new_tracker.state_6,
        }

    else:
        return {
            "state_1": tracker.state_1,
            "state_2": tracker.state_2,
            "state_3": tracker.state_3,
            "state_4": tracker.state_4,
            "state_5": tracker.state_5,
            "state_6": tracker.state_6,
        }

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
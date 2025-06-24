import os

from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, or_, String, text
from sqlalchemy.ext.asyncio import AsyncSession

from database import init_db, get_db, async_session
from models import User, Tracker
from schemas import UserCreate, UserResponse
import requests

from state_config import STATE_DETAILS

app = FastAPI()
scheduler = AsyncIOScheduler()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
MAX_RETRIES = 5
INITIAL_DELAY = 1  # seconds
EXTERNAL_TIMEOUT = 10  # seconds



async def send_telegram_message(chat_id: str, message: str):
    async with ClientSession() as session:
        await session.post(
            TELEGRAM_API_URL,
            json={"chat_id": chat_id, "text": message}
        )

async def update_null_trackers():
    async with async_session() as db:
        stmt = select(Tracker).where(
            or_(
                Tracker.state_6 == None,  # SQL NULL
                Tracker.state_6.cast(String) == text("'null'")  # JSON null (as text)
            )
        )
        result = await db.execute(stmt)
        trackers = result.scalars().all()
        print(f"🔍 Найдено трекеров для обновления: {len(trackers)}")

        async with ClientSession() as http_session:
            for tracker in trackers:
                try:
                    async with http_session.post(
                        "http://147.45.147.92:1241/track",
                        json={"track": tracker.tracking_code}
                    ) as response:

                        if response.status != 200:
                            print(f"❌ Failed to fetch for {tracker.tracking_code}")
                            continue

                        data = await response.json()
                        info = data.get("info", {})
                        tracking_events = info.get("tracking", [])
                        print(tracking_events)
                        # сохранить старые состояния
                        old_states = [
                            tracker.state_1,
                            tracker.state_2,
                            tracker.state_3,
                            tracker.state_4,
                            tracker.state_5,
                            tracker.state_6,
                        ]

                        # собрать новые состояния (до 6)
                        new_states = []
                        for i, event in enumerate(reversed(tracking_events[:6])):
                            state_key = f"state_{i + 1}"
                            new_states.append({
                                "details": STATE_DETAILS.get(state_key),
                                "date": event.get("date")
                            })

                        while len(new_states) < 6:
                            new_states.append(None)

                        # обновить трекер
                        tracker.state_1 = new_states[0]
                        tracker.state_2 = new_states[1]
                        tracker.state_3 = new_states[2]
                        tracker.state_4 = new_states[3]
                        tracker.state_5 = new_states[4]
                        tracker.state_6 = new_states[5]

                        # найти обновлённые поля
                        updated_fields = []
                        for i, (old, new) in enumerate(zip(old_states, new_states), start=1):
                            if old is None and new is not None:
                                updated_fields.append(
                                    f"🆕 state_{i}: {new['details']} ({new['date']})"
                                )

                        # отправить уведомление
                        if updated_fields and tracker.telegram_chat_id:
                            message = f"📦 Обновление по треку {tracker.tracking_code}:\n" + "\n".join(updated_fields)
                            await send_telegram_message(tracker.telegram_chat_id, message)

                except Exception as e:
                    print(f"❌ Error with {tracker.tracking_code}: {e}")

            await db.commit()
        print("✅ Трекеры с пустыми состояниями обновлены.")

@app.on_event("startup")
async def on_startup():
    await init_db()
    scheduler.add_job(update_null_trackers, "interval", hours=1, misfire_grace_time=1800)
    scheduler.start()

@app.on_event("shutdown")
async def shutdown():
    scheduler.shutdown()

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
async def get_order_info(
        order_no: str,
        user_id: str,
        db: AsyncSession = Depends(get_db)
):
    # Check database first
    result = await db.execute(select(Tracker).where(Tracker.tracking_code == order_no))
    tracker = result.scalar_one_or_none()

    if tracker:
        return {f"state_{i}": getattr(tracker, f"state_{i}") for i in range(1, 7)}

    # External service request with retries
    async with httpx.AsyncClient(timeout=EXTERNAL_TIMEOUT) as client:
        delay = INITIAL_DELAY
        for attempt in range(MAX_RETRIES):
            try:
                response = await client.post(
                    "http://147.45.147.92:1241/track",
                    json={"track": order_no}
                )
                response.raise_for_status()
                data = response.json()

                # Check if expected data is present
                if "info" in data and "tracking" in data["info"]:
                    tracker_info = data["info"]
                    break

            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                last_error = e
                if attempt == MAX_RETRIES - 1:
                    raise HTTPException(
                        status_code=503,
                        detail=f"External service error: {str(e)}"
                    )

            # Exponential backoff before retry
            await asyncio.sleep(delay)
            delay *= 2
        else:
            raise HTTPException(
                status_code=504,
                detail="External service didn't return valid data after retries"
            )

    # Process tracking events
    tracking_events = tracker_info.get("tracking", [])[::-1][:6]  # Latest first
    states = []

    for i, event in enumerate(tracking_events):
        states.append({
            "details": STATE_DETAILS.get(f"state_{i + 1}"),
            "date": event.get("date")
        })

    # Pad remaining states
    states.extend([None] * (6 - len(states)))

    # Create and save new tracker
    new_tracker = Tracker(
        tracking_code=order_no,
        user_id=user_id,
        **{f"state_{i + 1}": state for i, state in enumerate(states)}
    )

    db.add(new_tracker)
    await db.commit()
    await db.refresh(new_tracker)

    return {f"state_{i}": getattr(new_tracker, f"state_{i}") for i in range(1, 7)}
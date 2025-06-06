# app/tasks.py
import asyncio
import requests
from celery import shared_task
from sqlalchemy.future import select

from .database import async_session
from .models import Tracker


@shared_task(name="tasks.update_null_states")
def update_null_states():
    print("update_null_states")
    asyncio.run(_update_states())


async def _update_states():
    print("_update_states")
    async with async_session() as session:
        result = await session.execute(
            select(Tracker).where(Tracker.state_6 == None)
        )
        trackers = result.scalars().all()
        print(trackers)
        for tracker in trackers:
            print(tracker.tracking_code)
            response = requests.post("http://147.45.147.92:1241/track", json={"track": tracker.tracking_code})
            if response.status_code != 200:
                print(f"Failed to update tracker {tracker.tracking_code}: {response.text}")
                continue

            tracker_info = response.json().get("info", {})
            tracking_events = tracker_info.get("tracking", [])

            # Build up to 6 latest states
            states = []
            for event in reversed(tracking_events[:6]):
                states.append({
                    "details": event.get("details"),
                    "date": event.get("date")
                })

            while len(states) < 6:
                states.append(None)

            tracker.state_1 = states[0]
            tracker.state_2 = states[1]
            tracker.state_3 = states[2]
            tracker.state_4 = states[3]
            tracker.state_5 = states[4]
            tracker.state_6 = states[5]

        await session.commit()

import os
import re
from typing import Optional
from urllib.parse import urljoin

from fastapi import FastAPI, Depends, Form, UploadFile, File, HTTPException
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from database import init_db, get_db
from models import Case
from schemas import CaseOut, CaseUpdate

app = FastAPI()
case_list_views = Counter(
    "case_list_views_total",
    "Статистика посещения страницы с кейсами"
)
case_detail_views = Counter(
    "case_detail_views_total",
    "Статистика по каждому кейсу",
    ["case_id"]  # добавляем лейбл case_id
)


Instrumentator().instrument(app).expose(app, endpoint="/metrics")
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.on_event("startup")
async def on_startup(db: AsyncSession = Depends(get_db)):
    await init_db()


@app.post("/case", response_model=CaseOut)
async def create_case_with_image(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    price_new: float = Form(...),
    price_old: float = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    safe_title = re.sub(r'[^\w\d_]', '_', title)
    safe_filename = re.sub(r'[^\w\d_.]', '_', image.filename)

    filename = f"{safe_title}_{safe_filename}"
    file_path = os.path.join("uploads", filename)

    with open(file_path, "wb") as f:
        f.write(await image.read())

    # Формируем URL
    image_url = f"uploads/{filename}"
    print(image_url)

    image_url = image_url.replace(" ", "_")
    print(image_url)
    # Создаем запись в БД
    new_case = Case(
        title=title,
        description=description,
        price_new=price_new,
        price_old=price_old,
        image_url=image_url
    )
    db.add(new_case)
    await db.commit()
    await db.refresh(new_case)
    image_url = str(request.base_url) + new_case.image_url

    return CaseOut(
        id=new_case.id,
        title=new_case.title,
        description=new_case.description,
        price_new=new_case.price_new,
        price_old=new_case.price_old,
        image_url=image_url
    )
@app.get("/cases")
async def get_all_cases(request: Request, db: AsyncSession = Depends(get_db)):
    case_list_views.inc()

    result = await db.execute(select(Case))
    cases = result.scalars().all()
    return [add_full_image_url(case, request) for case in cases]
@app.get("/cases/{case_id}")
async def get_case(case_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalar_one_or_none()
    if case:
        case_detail_views.labels(case_id=case_id).inc()
        return add_full_image_url(case, request)
    raise HTTPException(status_code=404, detail="Case not found")
@app.put("/cases/{case_id}")
async def update_case(
        case_id: int,
        request: Request,
        title: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        price_new: Optional[float] = Form(None),
        price_old: Optional[float] = Form(None),
        image: Optional[UploadFile] = File(None),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalars().first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    if title is not None:
        case.title = title
    if description is not None:
        case.description = description
    if price_new is not None:
        case.price_new = price_new
    if price_old is not None:
        case.price_old = price_old

    if image is not None:
        if case.image_url:
            old_file_path = os.path.join("uploads", os.path.basename(case.image_url))
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

        safe_title = re.sub(r'[^\w\d_]', '_', case.title)
        safe_filename = re.sub(r'[^\w\d_.]', '_', image.filename)
        filename = f"{safe_title}_{safe_filename}"
        file_path = os.path.join("uploads", filename)

        with open(file_path, "wb") as f:
            f.write(await image.read())

        case.image_url = f"uploads/{filename}".replace(" ", "_")

    await db.commit()
    await db.refresh(case)

    image_url = str(request.base_url) + case.image_url if case.image_url else None

    return CaseOut(
        id=case.id,
        title=case.title,
        description=case.description,
        price_new=case.price_new,
        price_old=case.price_old,
        image_url=image_url
    )
@app.delete("/cases/{case_id}")
async def delete_case(case_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    db_case = await get_case(case_id, request, db=db)
    if db_case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    await db.delete(db_case)
    await db.commit()
    return {"status": "deleted"}


def add_full_image_url(case: Case, request: Request):
    case.image_url = urljoin(str(request.base_url), case.image_url.lstrip("/"))
    return case
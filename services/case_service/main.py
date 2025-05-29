import hashlib
import os
import re
from typing import Optional, List
from urllib.parse import urljoin

from fastapi import FastAPI, Depends, Form, UploadFile, File, HTTPException
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from custom_static import CustomStaticFiles

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
app.mount("/uploads", CustomStaticFiles(directory="uploads"), name="uploads")

IMAGE_HOST = "http://89.23.116.157:8006"


@app.on_event("startup")
async def on_startup(db: AsyncSession = Depends(get_db)):
    await init_db()


@app.post("/case", response_model=CaseOut)
async def create_case_with_images(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    price_new: float = Form(...),
    price_old: float = Form(...),
    days: Optional[int] = Form(None),
    images: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    image_urls = []

    for image in images:
        image_url = await save_image(image, title)
        image_urls.append(image_url)

    new_case = Case(
        title=title,
        description=description,
        price_new=price_new,
        price_old=price_old,
        image_urls=image_urls,
        days=days
    )
    db.add(new_case)
    await db.commit()
    await db.refresh(new_case)

    full_urls = [build_image_url(url.split("/")[-1]) for url in new_case.image_urls]  # берём только имя файла

    return CaseOut(
        id=new_case.id,
        title=new_case.title,
        description=new_case.description,
        price_new=new_case.price_new,
        price_old=new_case.price_old,
        image_urls=full_urls,
        days=new_case.days
    )
@app.get("/cases")
async def get_all_cases(request: Request, db: AsyncSession = Depends(get_db)):
    case_list_views.inc()

    result = await db.execute(select(Case))
    cases = result.scalars().all()

    return [add_full_image_urls(case, request) for case in cases]

@app.get("/cases/{case_id}")
async def get_case(case_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalar_one_or_none()
    if case:
        case_detail_views.labels(case_id=case_id).inc()
        return add_full_image_urls(case, request)

    raise HTTPException(status_code=404, detail="Case not found")
@app.put("/cases/{case_id}", response_model=CaseOut)
async def update_case(
    case_id: int,
    request: Request,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price_new: Optional[float] = Form(None),
    price_old: Optional[float] = Form(None),
    days: Optional[int] = Form(None),
    images: Optional[List[UploadFile]] = File(None),
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
    if days is not None:
        case.days = days

    if images:
        # Удаляем старые изображения
        if case.image_urls:
            for img_path in case.image_urls:
                old_file_path = os.path.join("uploads", os.path.basename(img_path))
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

        # Сохраняем новые изображения
        new_image_urls = []
        for image in images:
            image_url = await save_image(image, title)
            new_image_urls.append(image_url)

        case.image_urls = new_image_urls

    await db.commit()
    await db.refresh(case)

    full_urls = [build_image_url(url.split("/")[-1]) for url in case.image_urls] if case.image_urls else []

    return CaseOut(
        id=case.id,
        title=case.title,
        description=case.description,
        price_new=case.price_new,
        price_old=case.price_old,
        image_urls=full_urls,
        days=case.days
    )

@app.delete("/cases/{case_id}")
async def delete_case(case_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    db_case = await get_case(case_id, request, db=db)
    if db_case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    await db.delete(db_case)
    await db.commit()
    return {"status": "deleted"}

def add_full_image_urls(case: Case, request: Request):
    case.image_urls = [build_image_url(url.split("/")[-1]) for url in case.image_urls]
    return case

async def save_image(image: UploadFile, title: str) -> str:
    content = await image.read()
    await image.seek(0)  # не забудь сбросить указатель, если файл потом сохраняется

    hash = hashlib.md5(content).hexdigest()[:8]  # короткий хеш
    ext = os.path.splitext(image.filename)[-1]
    safe_title = re.sub(r"[^\w\d_]", "_", title)
    filename = f"{safe_title}_{hash}{ext}"
    file_path = os.path.join("uploads", filename)

    with open(file_path, "wb") as f:
        f.write(content)

    return f"uploads/{filename}"

def build_image_url(filename: str) -> str:
    return f"{IMAGE_HOST}/uploads/{filename}"
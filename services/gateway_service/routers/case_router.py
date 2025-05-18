from fastapi import APIRouter, Request, Form, UploadFile, File
from typing import Optional
from fastapi.responses import JSONResponse
import httpx

CASE_SERVICE_URL = "http://case-service:8002"

router = APIRouter()

@router.get("/", summary="Get all cases")
async def get_all_cases():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{CASE_SERVICE_URL}/cases")
    return JSONResponse(content=resp.json(), status_code=resp.status_code)

@router.get("/{case_id}", summary="Get case by id")
async def get_case(case_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{CASE_SERVICE_URL}/cases/{case_id}")
    return JSONResponse(content=resp.json(), status_code=resp.status_code)

@router.post("/", summary="Create case")
async def create_case_with_image(title: str = Form(...),
    description: str = Form(...),
    price_new: float = Form(...),
    price_old: float = Form(...),
    image: UploadFile = File(...),):
    image_bytes = await image.read()

    form_data = {
        "title": (None, title),
        "description": (None, description),
        "price_new": (None, str(price_new)),
        "price_old": (None, str(price_old)),
        "image": (image.filename, image_bytes, image.content_type),
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{CASE_SERVICE_URL}/case",
            files=form_data
        )
    try:
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except Exception:
        return JSONResponse(content={"error": resp.text}, status_code=resp.status_code)

@router.delete("/{case_id}", summary="Delete case")
async def delete_case(case_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.delete(f"{CASE_SERVICE_URL}/cases/{case_id}")
    return JSONResponse(content=resp.json(), status_code=resp.status_code)

@router.put("/{case_id}", summary="Update case")
async def update_case(case_id: int,
        request: Request,
        title: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        price_new: Optional[float] = Form(None),
        price_old: Optional[float] = Form(None),
        image: Optional[UploadFile] = File(None),
):
    form_data = {}

    if title is not None:
        form_data["title"] = (None, title)
    if description is not None:
        form_data["description"] = (None, description)
    if price_new is not None:
        form_data["price_new"] = (None, str(price_new))
    if price_old is not None:
        form_data["price_old"] = (None, str(price_old))

    if image is not None:
        image_bytes = await image.read()
        form_data["image"] = (image.filename, image_bytes, image.content_type)

    async with httpx.AsyncClient() as client:
        resp = await client.put(
            f"{CASE_SERVICE_URL}/cases/{case_id}",
            files=form_data  # httpx treats this as multipart/form-data
        )

    try:
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except Exception:
        return JSONResponse(content={"error": resp.text}, status_code=resp.status_code)

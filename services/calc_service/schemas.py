from pydantic import BaseModel

class CalcRequest(BaseModel):
    weight: float  # в кг
    volume: float  # в м3
    cargo_type: str  # например "стандарт", "другое"

class CalcResponse(BaseModel):
    density: float
    price_per_kgm3: float
    total_price: float

class PriceRow(BaseModel):
    min: float
    max: float
    price: float
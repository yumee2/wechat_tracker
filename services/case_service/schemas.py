from pydantic import BaseModel
from typing import Optional, List


class CaseBase(BaseModel):
    title: str
    description: str
    price_new: float
    price_old: float
    image_urls: List[str]
    days: Optional[int]

class CaseCreate(CaseBase):
    pass

class CaseUpdate(CaseBase):
    pass

class CaseOut(CaseBase):
    id: int

    class Config:
        from_attributes = True
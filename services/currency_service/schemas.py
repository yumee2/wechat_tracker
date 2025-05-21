from pydantic import BaseModel


class CurrencyRate(BaseModel):
    pair: str
    rate: float
    type: str
    

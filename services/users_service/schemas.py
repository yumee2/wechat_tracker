from pydantic import BaseModel

class UserCreate(BaseModel):
    telegram_id: str
    username: str
    first_name: str

class UserResponse(BaseModel):
    id: int
    telegram_id: str
    username: str
    first_name: str
    is_admin: bool
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False)
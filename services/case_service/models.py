from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Case(Base):
    __tablename__ = "cases"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price_new = Column(Float, nullable=False)
    price_old = Column(Float, nullable=False)
    image_urls = Column(ARRAY(String))
    days = Column(Integer, nullable=True)
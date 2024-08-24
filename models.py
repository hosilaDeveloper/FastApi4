from sqlalchemy import Column, INTEGER, String, Float
from typing import Optional

from database import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    image = Column(String or None)

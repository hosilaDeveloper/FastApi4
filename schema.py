from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    price: int
    description: Optional[str] = None
    image: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

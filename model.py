from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    name: str
    age: int
    email: str


class Product(BaseModel):
    id: int | None = None
    name: str
    price: float
    in_stock: bool

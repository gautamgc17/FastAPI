# We will have the file models.py with the SQLAlchemy models, and the file schemas.py with the Pydantic models.

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool=True
    items: list[Item] = []

    class Config:
        orm_mode = True

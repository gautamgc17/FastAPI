from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr
from typing import Literal
app = FastAPI()


# response models
class UserIn(BaseModel):
    full_name: str
    email: EmailStr
    username: str

class UserHelper(UserIn):
    password: str

class UserOut(UserIn):
    pass

# password is not returned because of response_model 
@app.get("/user", response_model=UserOut)
async def show_user(user: UserHelper):
    return user

class Item(BaseModel):
    name: str
    description: str|None = None
    price: float
    tax: float = 18
    tags: list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 18, "tags": []},
}

@app.get("/item", response_model = Item, response_model_exclude_unset=True)
async def show_user(item: Literal["foo", "bar", "baz"]):
    return items[item]

@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_items_public_data(item_id: Literal["foo", "bar", "baz"]):
    return items[item_id]



# status code
@app.post("/items/", status_code = status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
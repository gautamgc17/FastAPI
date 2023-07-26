from datetime import datetime, time, timedelta
from enum import Enum
from typing import Literal, Union, List, Optional
from uuid import UUID

from fastapi import (FastAPI, Body, Query, Path, Cookie, Header, status, Form, File, UploadFile, Request)
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field, HttpUrl, EmailStr

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.exception_handlers import (http_exception_handler, request_validation_exception_handler)

from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import HTMLResponse

app = FastAPI()



# exception handling
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in range(0, 10):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Id not found!!" , headers={"X-Error":"There goes my error"})
    return {"message": item_id}



# custom exception handling class
class UnicornException(Exception):
    def __init__(self, name):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow.."}
    )

@app.get("/unicorns/{name}")
async def read_unicorns(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}



# overwriting exception handling class
@app.exception_handler(RequestValidationError)
async def http_exception_handler(request: Request, exc: RequestValidationError):
    print(dir(exc))
    return PlainTextResponse(str(exc.args[0][0]['msg']) , status_code=400)

@app.get("/validation_items/{item_id}")
async def read_validation_items(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}



# overwriting exception handling class
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "blahblah": exc.body}),
    )

class Item(BaseModel):
    title: str
    size: int

@app.post("/items/")
async def create_item(item: Item):
    return item



# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request, exc):
#     print(f"OMG! An HTTP error!: {repr(exc)}")
#     return await http_exception_handler(request, exc)


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     print(f"OMG! The client sent invalid data!: {exc}")
#     return await request_validation_exception_handler(request, exc)


# @app.get("/blah_items/{item_id}")
# async def read_items(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
#     return {"item_id": item_id}



# Path Operation Configuration
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

class Tags(Enum):
    items = "items"
    users = "users"

@app.post(
    "/items/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.items],
    summary="Create an Item-type item",
    # description="Create an item with all the information: "
    # "name; description; price; tax; and a set of "
    # "unique tags",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


@app.get("/items/", tags=[Tags.items])
async def read_items():
    return [{"name": "Foo", "price": 42}]

@app.get("/users/", tags=[Tags.users])
async def read_users():
    return [{"username": "PhoebeBuffay"}]




#  JSON Compatible Encoder and Body Updates - Put and Patch
class Product(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []

db = {"foo": {"name": "Foo", "price": 50.2} , "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},}

@app.put("/products/{prod_id}", response_model=Product)
async def update_item(prod_id: str, product: Product):
    json_compatible = jsonable_encoder(product)
    db[prod_id] = json_compatible
    print(db)
    return json_compatible

@app.patch("/products/{prod_id}", response_model=Product)
async def update_item(prod_id: str, product: Product):
    # find data , convert into model , body param to dict with exclude_unset, update model convert into json_encoder
    stored_data = db.get(prod_id, None)
    if stored_data is not None:
        stored_model = Product(**stored_data)
    else:
        stored_model = Product()
    print('1', stored_data)
    print('2', stored_model)
    print('3', product)

    update_data = product.dict(exclude_unset=True)
    updated_model = stored_model.model_copy(update=update_data)
    json_data = jsonable_encoder(updated_model)
    db[prod_id] = json_data

    print('4', json_data)
    return updated_model


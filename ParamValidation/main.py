from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from pydantic import BaseModel , Field , HttpUrl
from typing import Optional
from enum import Enum
from uuid import UUID
from datetime import datetime , timedelta , time , date

app = FastAPI()



# query parameters and string validation
@app.get("/items")
# async def read_items(query: list[str] = Query(default=[])):
async def read_items(query: str = Query(... , min_length=4 , max_length=10 , regex="^[a-zA-Z]+" , 
                                        description="Sample Query" , alias="item-query" , include_in_schema=False)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if query:
        results.update({"query": query})
    return results



# query + path parameters and integer validation
@app.get("/valid_items/{item_id}")
async def check_items(item_id: int = Path(..., lt=100, ge=10), item_size: float = Query(default=0.0, gt=5.75)):
    return {"item_id": item_id , "item_size": item_size} 



# multiple parameters
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

# * makes it keyworded arguments
# embed = True makes key-value in body parameter
@app.put("/items/{item_id}")
async def update_item(* , item_id: int = Path(..., title="The ID of the item to get", ge=0, le=150) , q: str | None = None , 
                      item: Item = Body(..., embed=True)):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results



# Body - Fields
class Item(BaseModel):
    name: str
    description: str | None = Field(None, title="The description of the item", max_length=300)
    price: float = Field(..., gt=0, description="The price must be greater than zero.")
    tax: float | None = None


@app.put("/itemsV2/{item_id}")
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results



# Nested Models
class Image(BaseModel):
    url: HttpUrl
    product_name: str

class Object(BaseModel):
    name: str
    description: str|None = None
    price: float
    tax: float|None = None
    tags: list[str] = []
    image: list[Image] | None = None

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]

@app.put("/object/{object_id}")
async def update_item(object_id: int, object: Object):
    return {"object_id": object_id , "object": object}

@app.post("/images/multiple")
async def create_multiple_images(images: list[Image]):
    return images

@app.post("/blah")
async def create_some_blahs(blahs: dict[str, float]):
    return blahs



# declare request example data
class Product(BaseModel):
    name: str = Field(... , examples=["george willey"])
    description: str|None = Field(None, examples=["This explains the product"])
    price: float = Field(... , examples=[20.25])
    tax: float|None = Field(None , examples=[5.45])

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "name": "Foo",
    #             "description": "A very nice Item",
    #             "price": 16.25,
    #             "tax": 1.67,
    #         }
    #     }

@app.put("/product/{product_id}")
async def products(product_id: int , prod: Product):
    return {"product_id": product_id , "product": prod}

@app.put("/product-new/{product_id}")
async def products(product_id: int , prod: Product = Body(... , example={"name": "Foo", "description": "A very nice Item","price": 16.25, "tax": 1.67})):
    return {"product_id": product_id , "product": prod}



# some other data types
@app.put("/sample/{item_id}")
async def read_items(item_id: UUID, start_date: datetime | None = Body(None), end_date: datetime | None = Body(None), 
                     repeat_at: time | None = Body(None), process_after: timedelta | None = Body(None)):
    
    start_process = start_date + process_after
    duration = end_date - start_process
    return {
        "item_id": item_id,
        "start_date": start_date,
        "end_date": end_date,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }



# cookie and header parameters
@app.get("/params")
async def read_items(cookie_id: str | None = Cookie(None), accept_encoding: str | None = Header(None), sec_ch_ua: str | None = Header(None), 
                     user_agent: str | None = Header(None), x_token: list[str] | None = Header(None)):
    return {
        "cookie_id": cookie_id,
        "Accept-Encoding": accept_encoding,
        "sec-ch-ua": sec_ch_ua,
        "User-Agent": user_agent,
        "X-Token values": x_token,
    }

# In order to set a custom header, its name should be prefixed with "X". In the following case, a custom header called "X-Web-Framework" and a predefined header “Content-Language" is added along with the response of the operation function.
from fastapi import FastAPI
from fastapi.responses import JSONResponse
app = FastAPI()
@app.get("/rspheader/")
def set_rsp_headers():
   content = {"message": "Hello World"}
   headers = {"X-Web-Framework": "FastAPI", "Content-Language": "en-US"}
   return JSONResponse(content=content, headers=headers)

 

from fastapi import FastAPI
from enum import Enum
from typing import Optional
from pydantic import BaseModel
app = FastAPI()


# HTTP GET method for the route "/" 
@app.get("/", description="This is our first route", deprecated=True)
async def main():
    return {"message": "Hello World"}

@app.post("/")
async def create():
    return {"message": "Hello World"}



# path parameters - {}
@app.get("/items")
async def list_items():
    return {"message": "This is items route"}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"message": item_id}



# create a collection of name/value pairs
class FoodEnum(Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"

@app.get("/foods/{food_name}")
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.fruits:
        return {"message": food_name}
    
    # the value of any enum member
    if food_name.value == "vegetables":
        return {"message": food_name}
    
    return {"message": food_name}



# query parameters are the things you see in a URL that go at the end and look like "?hello=world&foo=bar"
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}, {"item_name": "Woo"}, {"item_name": "War"}, {"item_name": "Waz"}]

@app.get("/list_items")
async def list_items(skip: int=0, limit: int=10):
    # this helps in limiting query results and pagination
    return fake_items_db[skip: skip+limit]

@app.get("/list_items/{item_id}")
async def get_item(item_id: int, query: str|None = None):
    if query:
        return {"message":item_id, "query":query}
    return {"message":item_id}

@app.get("/random/{item_id}")
async def get_item(item_id: int, req_param: str, query: str|None = None, extra: bool = False):
    res = {"message": item_id}
    if query:
        res.update({"query": query})
    if extra:
        res.update({"exyra description": "This is a sample"})
    return res



# base model class for creating Pydantic models - request body
class ItemModel(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float|None = None

@app.post("/all_items")
async def all_items(item: ItemModel):
    item_dict = item.dict()
    if item.tax:
        # this is attribute of our class and not actual dictionary
        updated_value = item.price + item.tax
        item_dict.update({"updated_price": updated_value})
        print(item_dict)
    return item_dict

@app.put("/all_items/{item_id}")
async def create_item_with_put(item_id: int, item: ItemModel, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result



from datetime import datetime, time, timedelta
from enum import Enum
from typing import Literal, Union, List, Optional, Annotated
from uuid import UUID

from fastapi import (FastAPI, Body, Query, Path, Cookie, Header, status, Form, File, UploadFile, HTTPException, Request, Depends)
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field, HttpUrl, EmailStr

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.exception_handlers import (http_exception_handler, request_validation_exception_handler)

from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import HTMLResponse

app = FastAPI()


# common functionalities being shared - dependency injection
async def hello():
    return "world"

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100, random: str = Depends(hello)):
    return {"q": q, "skip": skip, "limit": limit, "random": random}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons



# class dependecies - takes the items in constructor to create parameters
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonParams:
    def __init__(self, query_id: int, q: str|None=None, skip: int=0, limit: int=10):
        self.q = q
        self.skip = skip
        self.limit = limit
        self.query_id = query_id

@app.get("/query/{query_id}")
async def get_samples(commons = Depends(CommonParams)):
    response = {}
    print(commons.query_id)
    if commons.q:
        response.update({"query": commons.q})
    items_db = fake_items_db[commons.skip:commons.skip+commons.limit]
    response.update({"items": items_db})
    return response



# Sub-Dependencies
def query_extractor(q: str | None = None):
    return q

def query_or_body_extractor(q: str = Depends(query_extractor), last_query: str | None = Body(None)):
    if q:
        return q
    return last_query

@app.post("/item")
async def try_query(query_or_body: str = Depends(query_or_body_extractor)):
    return {"q_or_body": query_or_body}


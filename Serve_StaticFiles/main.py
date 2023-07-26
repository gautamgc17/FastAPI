from fastapi import FastAPI , Request , Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates("templates")
app.mount("/static" , StaticFiles(directory="static") , name = "static")

@app.get("/hello/{name}", response_class=HTMLResponse)
async def hello(request: Request , name:str):
   return templates.TemplateResponse(name = "hello.htm" , context = {"request": request , "username": name, "range": range(0, 5)})


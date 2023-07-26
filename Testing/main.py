# import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="ChimichangApp",
    description="This is an example of metadata about the app",
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

@app.get("/greet/{name}")
async def greet(name: str):
    return {"hello": name}





# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI , Form , Body , File , UploadFile
from pydantic import BaseModel

app = FastAPI()

# Form Fields
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    print("password", password)
    return {"username": username}

@app.post("/login-json/")
async def login_json(username: str = Body(...), password: str = Body(...)):
    print("password", password)
    return {"username": username}

class User(BaseModel):
   username:str
   password:str

@app.post("/submit/", response_model=User)
async def submit(nm: str = Form(...), pwd: str = Form(...)):
   return User(username=nm, password=pwd)



# Request Files
@app.post("/file/")
async def file_upload(file: bytes = File(...)):
    return len(file)

@app.post("/uploadFile/")
async def file_upload_v1(file: UploadFile|None = None):
    if not file:
        return "No file has been uploaded!!"
    contents = await file.read()
    return file.filename

@app.post("/uploadFiles/")
async def file_upload_v2(files: list[UploadFile] = File(... , description="Upload the files here")):
    return [file.filename for file in files]



# Request Forms and Files
@app.post("/files/")
async def create_file(file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...), hello: str = Body(...)):
    return {
        "file_size": len(file),
        "fileb_content_type": fileb.content_type,
        # here it will not be body parameter in json type but multipart/form-data
        "token": token,
        "hello": hello,
    }


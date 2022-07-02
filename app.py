import uvicorn
from fastapi import FastAPI, Depends, Request, Form, status, File, UploadFile, staticfiles

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

from os.path import isfile, join
import os

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

# docs disabled, api is not restful
# using get request to delete might be disturbing
app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/templates", staticfiles.StaticFiles(directory='templates'), name="templates")
app.mount("/dl", staticfiles.StaticFiles(directory='uploads'), name="files")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fullpath():
    return os.path.abspath(os.path.dirname(__file__)) + "/uploads/"

def listdir():
    files = [f for f in os.listdir(fullpath()) if isfile(join(fullpath(), f))]
    return files

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    msgs = db.query(models.Text).all()
    files = listdir()
    return templates.TemplateResponse("home.html",
                                      {"request": request, "msg_list": msgs, "files_list": files})

@app.post("/add")
def add(request: Request, msg: str = Form('None'), db: Session = Depends(get_db)):
    if msg != "None":
        new_msg = models.Text(msg=msg)
        db.add(new_msg)
        db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{text_id}")
def delete(request: Request, text_id: int, db: Session = Depends(get_db)):
    text = db.query(models.Text).filter(models.Text.id == text_id).first()
    db.delete(text)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open(fullpath()+file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        await file.close()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@app.get("/deletefile/{filename}")
def deletefile(request: Request, filename: str):
    if os.path.exists(fullpath()+filename):
        os.remove(fullpath()+filename)

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, log_level="info")
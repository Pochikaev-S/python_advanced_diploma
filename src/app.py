from typing import List

from fastapi import FastAPI, File, UploadFile, APIRouter, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from fastapi.templating import Jinja2Templates


import schemas
import models

app = FastAPI()

templates = Jinja2Templates(directory='../templates')
app.mount("/static", StaticFiles(directory="../templates"), 'static')


@app.get('/')
async def get_main_page(request: Request):
    print(request.headers)
    return templates.TemplateResponse(name='index.html', context={'request': request})

@app.get('/api/users/me')
def dd(request: Request):
    print(request.headers)
    return templates.TemplateResponse(name='index.html', context={'request': request})



# uvicorn app:app --reload

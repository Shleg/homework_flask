from fastapi import FastAPI, Request, HTTPException, Form
from pydantic import BaseModel, EmailStr
import logging

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str


users = []


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # logger.info(f'Обработан запрос для {name}')
    return templates.TemplateResponse("base.html", {"request": request, "users": users})


@app.get('/add_user/', response_class=HTMLResponse)
async def get_form_add(request: Request):
    return templates.TemplateResponse("add_user.html", {"request": request})


@app.post('/add_user/')
async def add_user(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...),
                   confirm_password: str = Form(...)):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    user_id = len(users) + 1
    new_user = User(id=user_id, name=name, email=email, password=password)
    users.append(new_user)

    return templates.TemplateResponse("add_user.html", {"request": request, "name": name})


@app.put("/update_user/{user_id}")
async def update_task(user_id: int, user: User):
    for i in range(len(users)):
        if users[i].id == user_id:
            users[i] = user
    return user


@app.delete("/del_user/{user_id}")
async def del_user(user_id: int):
    for i in range(len(users)):
        if users[i].id == user_id:
            return {"item_id": users.pop(i)}
    return HTTPException(status_code=404, detail='Task not found')

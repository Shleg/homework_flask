"""
Разработать API для управления списком задач с использованием базы данных MongoDB. Для этого создайте
модель Task со следующими полями:
○ id: str (идентификатор задачи, генерируется автоматически)
○ title: str (название задачи)
○ description: str (описание задачи)
○ done: bool (статус выполнения задачи)
"""

from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field


class TaskIn(BaseModel):
    title: str = Field(..., max_length=32)
    desc: str = Field(max_length=100)
    done: bool


class Task(TaskIn):
    id: int


DATABASE_URL = "sqlite:///mydatabase.db"  # в корневой диретории создается файлом БД
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(32)),
    sqlalchemy.Column("desc", sqlalchemy.String(100)),
    sqlalchemy.Column("done", sqlalchemy.Boolean)
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={
    "check_same_thread": False})  # параметр check_same_thread нужен для работы с SQLite

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/tasks/', response_model=List[Task])
async def get_tasks():
    query = tasks.select()
    return await database.fetch_all(query)


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    query = tasks.select().where(tasks.c.id == task_id)
    return await database.fetch_one(query)


@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskIn):
    query = tasks.insert().values(**task.model_dump())
    last_record_id = await database.execute(query)
    return await get_task(last_record_id)


@app.put('/tasks/{task_id}', response_model=Task)
async def update_task(task_id: int, new_task: TaskIn):
    query = tasks.update().where(tasks.c.id == task_id).values(**new_task.model_dump())
    await database.execute(query)
    return await get_task(task_id)


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(query)
    return {'message': 'Task deleted'}

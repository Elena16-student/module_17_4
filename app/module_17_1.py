# В файле module_17_1.py создайте сущность FastAPI(), напишите один маршрут для неё - '/',
# по которому функция возвращает словарь - {"message": "Welcome to Taskmanager"}.
# Импортируйте объекты APIRouter и подключите к ранее созданному приложению FastAPI,
# объединив все маршруты в одно приложение.

from fastapi import FastAPI
from app.routers import task, user
#from app.models import *



app = FastAPI()

@app.get('/')
async def welcome():
    return {'message': 'Welcome to Taskmanager'}

app.include_router(task.router)
app.include_router(user.router)

#python -m uvicorn app.module_17_1:app --reload

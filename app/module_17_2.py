
from fastapi import FastAPI
from app.routers import task, user
from app.models import *

app = FastAPI()

@app.get('/')
async def welcome():
    return {'message': 'Welcome to Taskmanager'}

app.include_router(task.router)
app.include_router(user.router)


#python -m uvicorn app.module_17_2:app --reload

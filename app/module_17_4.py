from fastapi import FastAPI
from pydantic.v1.schema import schema

from app.routers import task, user


app = FastAPI()


@app.get('/')
async def welcome():
    return {'message': 'Welcome to Taskmanager'}


app.include_router(task.router)
app.include_router(user.router)

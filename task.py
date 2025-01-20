# В модуле task.py напишите APIRouter с префиксом '/task'
# и тегом 'task',
# а также следующие маршруты, с пустыми функциями:
#
# get '/' с функцией all_tasks.
# get '/task_id' с функцией task_by_id.
# post '/create' с функцией create_task.
# put '/update' с функцией update_task.
# delete '/delete' с функцией delete_task.

# from fastapi import APIRouter
#
# router=APIRouter(prefix='/task', tags=['task'])
#
# @router.get('/')
# async def all_tasks():
#     pass
#
# @router.get('/task_id')
# async def task_by_id():
#     pass
#
# @router.post('/create')
# async def create_task():
#     pass
#
# @router.put('/update')
# async def update_task():
#     pass
#
# @router.delete('/delete')
# async def delete_task():
#     pass

from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import *
#from app.routers import *
from app.schemas import CreateTask, UpdateTask
# Функции работы с записями.
from sqlalchemy import insert, select
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_task(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    tasks = db.query(User).filter(Task.id == task_id).first()
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task was not found')
    else:
        return tasks


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    users = db.scalars(select(User).where(User.id == user_id))
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    db.execute(insert(Task).values(title=create_task.title,
                                   content=create_task.content,
                                   priority=create_task.priority,
                                   user_id=user_id,
                                   slug=slugify(create_task.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], update_task: UpdateTask, task_id: int):
    tasks = db.query(Task).filter(Task.id == task_id).one_or_none()
    if tasks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task was not found')
        db.execute(update(Task).where(Task.id == task_id).values
               (title=update_task.title,
                content=update_task.content,
                priority=update_task.priority))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    tasks = db.query(Task).filter(Task.id == task_id).one_or_none()
    if tasks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task was not found')
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
# # В модуле user.py напишите APIRouter с префиксом '/user'
# # и тегом 'user', а также следующие маршруты, с пустыми функциями:
# # get '/' с функцией all_users.
# # get '/user_id' с функцией user_by_id.
# # post '/create' с функцией create_user.
# # put '/update' с функцией update_user.
# # delete '/delete' с функцией delete_user.
#
# from fastapi import APIRouter
#
# router=APIRouter(prefix='/user', tags=['user'])
#
# @router.get('/')
# async def all_users():
#     pass
#
# @router.get('/user_id')
# async def user_by_id():
#     pass
#
# @router.post('/create')
# async def create_user():
#     pass
#
# @router.put('/update')
# async def update_user():
#     pass
#
# @router.delete('/delete')
# async def delete_user():
#     pass
# Необходимо описать логику функций в user.py используя ранее написанные маршруты FastAPI.
# Подготовка:
# Для этого задания установите в виртуальное окружение пакет python-slugify.
# Скачайте этот файл, в нём описана функция-генератор для подключения к БД. Добавьте его в директорию backend.
# Подготовьтесь и импортируйте все необходимые классы и функции (ваши пути могут отличаться):
# Сессия БД
# Функция подключения к БД
# from backend.db_depends import get_db
# # Аннотации, Модели БД и Pydantic.
# from typing import Annotated
# from models import User
# Функции работы с записями.
# Функция создания slug-строки
#
# 17_4 Напишите логику работы функций маршрутов:
# Каждая из нижеперечисленных функций подключается к базе данных в момент обращения при помощи функции get_db - Annotated[Session, Depends(get_db)]
# Функция all_users ('/'):
# Должна возвращать список всех пользователей из БД. Используйте scalars, select и all
# Функция user_by_id ('/user_id'):
# Для извлечения записи используйте ранее импортированную функцию select.
# Дополнительно принимает user_id.
# Выбирает одного пользователя из БД.
# Если пользователь не None, то возвращает его.
# В противном случае выбрасывает исключение с кодом 404 и описанием "User was not found"
# Функция craete_user ('/create'):
# Для добавления используйте ранее импортированную функцию insert.
# Дополнительно принимает модель CreateUser.
# Подставляет в таблицу User запись значениями указанными в CreateUser.
# В конце возвращает словарь {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
# Обработку исключения существующего пользователя по user_id или username можете сделать по желанию.
# Функция update_user ('/update'):
# Для обновления используйте ранее импортированную функцию update.
# Дополнительно принимает модель UpdateUser и user_id.
# Если находит пользователя с user_id, то заменяет эту запись значениям из модели UpdateUser. Далее возвращает словарь {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
# В противном случае выбрасывает исключение с кодом 404 и описанием "User was not found"
# Функция delete_user ('/delete'):
# Для удаления используйте ранее импортированную функцию delete.
# Всё должно работать аналогично функции update_user, только объект удаляется.
# Исключение выбрасывать то же.
# Создайте, измените и удалите записи через интерфейс Swagger:
# Создайте 3 записи User с соответствующими параметрами:
# username: user1, user2, user3
# firstname: Pasha, Roza, Alex
# lastname: Technique, Syabitova, Unknown
# age: 40, 62, 25
# Измените запись с id=3: firstname = Bear, lastname = Grylls, age = 50
# Удалите запись с id =2.
# Выведите всех пользователей.
# Проверьте, выбрасываются ли исключения в ваших запросах.

from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import *
#from app.routers import *
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_user(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    else:
        return user


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    existing_user = db.query(User).filter_by(username=create_user.username).first()
    if existing_user is not None:
        return {'status_code': status.HTTP_409_CONFLICT,
                'transaction': f'User with username {create_user.username} already exists.'},
    else:
        db.execute(insert(User).values(username=create_user.username,
                                       firstname=create_user.firstname,
                                       lastname=create_user.lastname,
                                       age=create_user.age,
                                       slug=slugify(create_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], update_user: UpdateUser, user_id: int):
    user = db.query(User).filter(User.id == user_id).one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    else:
        db.execute(update(User).where(User.id == user_id).values
                   (firstname=update_user.firstname,
                    lastname=update_user.lastname,
                    age=update_user.age))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.query(User).filter(User.id == user_id).one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    else:
        tasks = db.query(Task).filter(Task.user_id == user_id).one_or_none()
        if tasks is not None:
            db.execute(delete(Task).where(Task.user_id == user_id))
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}


@router.get('/user_id/tasks')
async def task_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.query(User).filter(User.id == user_id).one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User was not found')
    task = db.query(Task).filter(Task.user_id == user_id).one_or_none()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task was not found')
    return task
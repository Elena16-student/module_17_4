from app.backend.db import Base
from sqlalchemy import Integer, ForeignKey, Column, String, Boolean
from sqlalchemy.orm import relationship
from app.models import*


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key = True, index=True) #целое число, первичный ключ, с индексом.
    username = Column(String) #строка.
    firstname = Column(String) #строка.
    lastname = Column(String) #строка.
    age = Column(Integer)
    slug = Column(String, unique = True, index=True)# строка, уникальная, с индексом.
    tasks = relationship('Task', back_populates='users')

from sqlalchemy.schema import CreateTable
print(CreateTable(User.__table__))

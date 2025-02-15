from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from pydantic import BaseModel
from typing import Optional

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key = True, index = True)
#     username = Column(String, unique=True, index=True)
#     password = Column(String)
    
#modelo user
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    

class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    url = Column(String, unique=True)

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,autoincrement=True)
    email = Column(String(100), unique=True)
    full_name = Column(String(100))
    password = Column(String(100))
    disabled = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

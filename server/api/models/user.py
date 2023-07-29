from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    firstname = Column(String(100))
    lastname = Column(String(100))
    hashed_password = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(100), unique=True, index=True)
    role = Column(String(100))
    status = Column(Boolean, default=True)
    photo = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

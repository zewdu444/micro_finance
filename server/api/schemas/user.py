from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
import datetime

class Role(str, Enum):
   admin = "admin"
   client = "client"

class UserCreate(BaseModel):
    username: str = Field(..., example="zewdu4")
    firstname: str = Field(..., example="Zewdu")
    lastname: str = Field(..., example="Abebe")
    email: EmailStr = Field(..., example="zewdu444@gmail.com")
    phone: str = Field(..., example="+251911223344")
    role : Role = Field(..., example="admin")
    photo: Optional[str] = Field(None, example="www.example.jpg")
    hashed_password: str = Field(..., example="123456")

class User(BaseModel):
    id: int = Field(..., example=1)
    username: str = Field(..., example="zewdu4")
    firstname: str = Field(..., example="Zewdu")
    lastname: str = Field(..., example="Abebe")
    email: EmailStr = Field(..., example="zewdu444@gmail.com")
    phone: str = Field(..., example="+251911223344")
    role : Role = Field(..., example="admin")
    photo: Optional[str] = Field(None, example="www.example.jpg")
    status: bool = Field(..., example=True)
    created_at: datetime.datetime = Field(...)
    updated_at: datetime.datetime = Field(...)







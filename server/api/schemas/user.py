from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
import datetime

class Role(str, Enum):
   admin = "admin"
   client = "client"

class Status(str, Enum):
    active ="active"
    inactive = "inactive"

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
    user_id: int = Field(..., example=1)
    username: str = Field(..., example="zewdu4")
    firstname: str = Field(..., example="Zewdu")
    lastname: str = Field(..., example="Abebe")
    email: EmailStr = Field(..., example="zewdu444@gmail.com")
    phone: str = Field(..., example="+251911223344")
    role : Role = Field(..., example="admin")
    photo: Optional[str] = Field(None, example="www.example.jpg")
    user_status: Status = Field(..., example="active")
    created_at: datetime.datetime = Field(...)
    updated_at: datetime.datetime = Field(...)

class UserUpdate(BaseModel):
    firstname:Optional[str] = Field(None, example="Zewdu")
    lastname: Optional[str] = Field(None, example="Abebe")
    email: Optional[EmailStr] = Field(None, example="zewdu444@gmail.com")
    phone: Optional[str] = Field(None, example="+251911223344")
    role : Optional[Role] = Field(None, example="admin")
    user_status: Optional[Status] = Field(None, example="active")
    photo: Optional[str] = Field(None, example="www.example.jpg")

class UserResetPassword(BaseModel):
     password: str = Field(..., example="123456")
     confirm_password: str = Field(..., example="123456")






from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import List, Dict

class BodyExample(BaseModel):
    username: str
    title: str
    message: str
    message_below: str
    link: HttpUrl

class PasswordRequestSchema(BaseModel):
    email: List[EmailStr] = Field(..., example=["zewdu.erkyhun@yandex.com"])
    subject: str = Field(..., example="Password Reset Request for Your Account")
    body: Dict[str, BodyExample] = Field(
        ...,
        example={
            "data": {
                "username": "zewdu erkyhun",
                "title": "Password Reset Request",
                "message": "You're receiving this email because you requested a password reset for your account.",
                "message_below": "If you didn't request a password reset you can safely ignore this email.",
                "link": "https://portfolio-cpgd.onrender.com/"
            }
        }
    )

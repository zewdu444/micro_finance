from pydantic import EmailStr, BaseModel, Field
from typing import List, Dict

class PasswordRequest(BaseModel):
    email: List[EmailStr] = Field(..., examples=["zewdu.erkyhun@yandex.com"])
    subject: str = Field(..., examples="Password Reset Request for Your Account" )
    body: Dict[str, str] = Field(...,examples={{
                    "username": "zewduerkyhun",
                    "title": "Password Reset Request",
                    "message": "You're receiving this email because you requested a password reset for your account.",
                    "message_below": "If you didn't request a password reset you can safely ignore this email.",
                    "link": "https://portfolio-cpgd.onrender.com/"
                }})

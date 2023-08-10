from pydantic import EmailStr, BaseModel, Field
from typing import List, Dict

class EmailSchema(BaseModel):
    email: List[EmailStr] = Field(...)
    subject: str = Field(...)
    body: Dict[str, str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": ["zewdu.erkyhun@yandex.com"],
                "subject": "FastAPI is Awesome!!",
                "body": {
                    "title": "FastAPI MAILER",
                    "message": "This email is sent by FastAPI"
                }
            }
        }

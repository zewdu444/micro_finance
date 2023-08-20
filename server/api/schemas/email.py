from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import List, Dict

class BodySchema(BaseModel):
    username: str
    title: str
    message: str
    message_below: str
    link: HttpUrl

class LoanSchema(BaseModel):
        loan_id: int = Field(..., example=1)
        member_name: str = Field(..., example="Zewdu Erkyhun")
        member_phone : str = Field(..., example="+251911223344")
        loan_type: str = Field(..., example="personal")
        loan_term: int = Field(..., example=12)
        requested_amount: float = Field(..., example=10000.00)
        interest_rate: float = Field(..., example=0.15)
        total_to_pay: float = Field(..., example=11500.00)
        total_interest: float = Field(..., example=1500.00)
        per_month_payment: float = Field(..., example=958.33)
        loan_status: str = Field(..., example="created")
        total_paid: float = Field(..., example=0.00)
        total_remaining: float = Field(..., example=11500.00)

class PasswordRequestSchema(BaseModel):
    email: List[EmailStr] = Field(..., example=["zewdu.erkyhun@yandex.com"])
    subject: str = Field(..., example="Password Reset Request for Your Account")
    body: Dict[str, BodySchema] = Field(
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

class LoanRequestSchema(BaseModel):
    email: List[EmailStr] = Field(..., example=["zewdu.erkyhun@yandex.com"] )
    subject: str = Field(..., example="Loan Registration")
    body: Dict[str, LoanSchema] = Field(
        ...,
        example={
            "data": {
                "loan_id": "1",
                "member_name": "Zewdu Erkyhun",
                "member_phone": "+251911223344",
                "loan_type": "personal",
                "loan_term": "12",
                "requested_amount": "10000.00",
                "interest_rate": "0.15",
                "total_to_pay": "11500.00",
                "total_interest": "1500.00",
                "per_month_payment": "958.33",
                "loan_status": "created",
                "total_paid": "0.00",
                "total_remaining": "11500.00"
            }
        }
    )

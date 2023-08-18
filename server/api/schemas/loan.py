from pydantic import BaseModel, EmailStr, Field, FiniteFloat
from typing import Optional
from enum import Enum
import datetime
from .member import Member
from .user import User
class LoanStatus(str, Enum):
    created = "created"
    applicated_submitted = "applicated_submitted"
    under_review = "under_review"
    document_pending = "document_pending"
    approved = "approved"
    rejected = "rejected"
    loan_disbursed = "loan_disbursed"
    in_payment = "in_payment"
    late_payment = "late_payment"
    completed = "completed"
    defaulted = "defaulted"
    closed = "closed"

class LoanType(str, Enum):
    emergency = "emergency"
    personal = "personal"
    business = "business"
    mortgage = "mortgage"
    auto = "auto"
    student = "student"
    debt_consolidation = "debt_consolidation"
    home_improvement = "home_improvement"
    other = "other"

class TransactionType(str, Enum):
    deposit = "deposit"
    withdraw = "withdraw"

class LoanApplicationCreate(BaseModel):
    member_id: int = Field(..., example=1)
    loan_type: LoanType = Field(..., example="personal")
    loan_term: FiniteFloat = Field(..., example=12)
    requested_amount: FiniteFloat = Field(..., example=10000.00)
    interest_rate: FiniteFloat = Field(..., example=0.15)
    related_document: Optional[str] = Field(None, example="www.example.jpg")

class LoanApplicationUpdate(BaseModel):
    loan_type: Optional[LoanType] = Field(None, example="personal")
    loan_term: Optional[FiniteFloat] = Field(None, example=12)
    requested_amount: Optional[FiniteFloat] = Field(None, example=10000.00)
    interest_rate: Optional[FiniteFloat] = Field(None, example=0.15)
    loan_status: Optional[LoanStatus] = Field(None, example="created")
    is_closed: Optional[bool] = Field(None, example=False)
    related_document: Optional[str] = Field(None, example="www.example.jpg")

class LoanApplication(BaseModel):
      loan_id: int = Field(..., example=1)
      member_id: Member
      loan_type: LoanType = Field(..., example="personal")
      loan_term: FiniteFloat = Field(..., example=12)
      requested_amount: FiniteFloat = Field(..., example=10000.00)
      interest_rate: FiniteFloat = Field(..., example=0.15)
      total_to_pay: FiniteFloat = Field(..., example=11500.00)
      total_interest: FiniteFloat = Field(..., example=1500.00)
      per_month_payment: FiniteFloat = Field(..., example=958.33)
      total_paid: FiniteFloat = Field(..., example=0.00)
      total_remaining: FiniteFloat = Field(..., example=11500.00)
      loan_status: LoanStatus = Field(..., example="created")
      is_closed: bool = Field(..., example=False)
      related_document: Optional[str] = Field(None, example="www.example.jpg")
      created_at: datetime.datetime = Field(...)
      updated_at: datetime.datetime = Field(...)
      created_by: User
      updated_by: User

class LoanTransactionCreate(BaseModel):
    transaction_type: TransactionType = Field(..., example="deposit")
    amount: FiniteFloat = Field(..., example=10000.00)
    description: Optional[str] = Field(None, example="deposit")
    source_account: Optional[str] = Field(None, example="CBE-1234567890")
    destination_account: Optional[str] = Field(None, example="CBE-1234567890")
    related_document: Optional[str] = Field(None, example="www.example.jpg")

class LoanTransactionUpdate(BaseModel):
    transaction_type: Optional[TransactionType] = Field(None, example="deposit")
    amount: Optional[FiniteFloat] = Field(None, example=10000.00)
    description: Optional[str] = Field(None, example="deposit")
    source_account: Optional[str] = Field(None, example="CBE-1234567890")
    destination_account: Optional[str] = Field(None, example="CBE-1234567890")
    related_document: Optional[str] = Field(None, example="www.example.jpg")

class LoanTransaction(BaseModel):
      transaction_id: int = Field(..., example=1)
      loan_id: int = Field(..., example=1)
      transaction_type: TransactionType = Field(..., example="deposit")
      amount: FiniteFloat = Field(..., example=10000.00)
      description: Optional[str] = Field(None, example="deposit")
      source_account: Optional[str] = Field(None, example="CBE-1234567890")
      destination_account: Optional[str] = Field(None, example="CBE-1234567890")
      related_document: Optional[str] = Field(None, example="www.example.jpg")
      created_at: datetime.datetime = Field(...)
      updated_at: datetime.datetime = Field(...)
      created_by: User
      updated_by: User



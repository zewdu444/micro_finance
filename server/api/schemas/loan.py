from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal
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
    requested_amount: Decimal = Field(..., example=10000.00)
    interest_rate: Decimal = Field(..., example=0.15)
    loan_status: LoanStatus = Field(..., example="created")
    is_closed: bool = Field(..., example=False)
    related_document: Optional[str] = Field(None, example="www.example.jpg")

class LoanApplicationUpdate(BaseModel):
    loan_type: Optional[LoanType] = Field(None, example="personal")
    requested_amount: Optional[Decimal] = Field(None, example=10000.00)
    interest_rate: Optional[Decimal] = Field(None, example=0.15)
    loan_status: Optional[LoanStatus] = Field(None, example="created")
    is_closed: Optional[bool] = Field(None, example=False)
    related_document: Optional[str] = Field(None, example="www.example.jpg")

class LoanApplication(BaseModel):
      loan_id: int = Field(..., example=1)
      member_id: Member
      loan_type: LoanType = Field(..., example="personal")
      requested_amount: Decimal = Field(..., example=10000.00)
      interest_rate: Decimal = Field(..., example=0.15)
      loan_status: LoanStatus = Field(..., example="created")
      is_closed: bool = Field(..., example=False)
      related_document: Optional[str] = Field(None, example="www.example.jpg")
      created_at: datetime.datetime = Field(...)
      updated_at: datetime.datetime = Field(...)
      created_by: User
      updated_by: User

class LoanTransactionCreate(BaseModel):
    loan_id: int = Field(..., example=1)
    transaction_type: TransactionType = Field(..., example="deposit")
    amount: Decimal = Field(..., example=10000.00)
    description: Optional[str] = Field(None, example="deposit")
    source_account: Optional[str] = Field(None, example="CBE-1234567890")
    destination_account: Optional[str] = Field(None, example="CBE-1234567890")
    related_document: Optional[str] = Field(None, example="www.example.jpg")

class LoanTransactionUpdate(BaseModel):
    transaction_type: Optional[TransactionType] = Field(None, example="deposit")
    amount: Optional[Decimal] = Field(None, example=10000.00)
    description: Optional[str] = Field(None, example="deposit")
    source_account: Optional[str] = Field(None, example="CBE-1234567890")
    destination_account: Optional[str] = Field(None, example="CBE-1234567890")
    related_document: Optional[str] = Field(None, example="www.example.jpg")

class LoanTransaction(BaseModel):
      transaction_id: int = Field(..., example=1)
      loan_id: LoanApplication
      transaction_type: TransactionType = Field(..., example="deposit")
      amount: Decimal = Field(..., example=10000.00)
      description: Optional[str] = Field(None, example="deposit")
      source_account: Optional[str] = Field(None, example="CBE-1234567890")
      destination_account: Optional[str] = Field(None, example="CBE-1234567890")
      related_document: Optional[str] = Field(None, example="www.example.jpg")
      created_at: datetime.datetime = Field(...)
      updated_at: datetime.datetime = Field(...)
      created_by: User
      updated_by: User



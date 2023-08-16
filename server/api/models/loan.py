from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime


class Loan_applications(Base):
    __tablename__ = "loan_applications"
    loan_id = Column(Integer, primary_key=True, index=True)
    loan_type = Column(String)
    requested_amount = Column(Float)
    interest_rate = Column(Float)
    loan_status = Column(String)
    is_closed = Column(Boolean)
    related_document = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.user_id"))
    updated_by = Column(Integer, ForeignKey("users.user_id"))
    created_by_user = relationship("Users", foreign_keys=[created_by], back_populates="created_loan_applications")
    updated_by_user = relationship("Users", foreign_keys=[updated_by], back_populates="updated_loan_applications")
    loan_transactions = relationship("Loan_transactions", back_populates="loan_application")

class Loan_transactions(Base):
  __tablename__ = "loan_transactions"
  transaction_id = Column(Integer, primary_key=True, index=True)
  loan_id = Column(Integer, ForeignKey("loan_applications.loan_id"))
  transaction_type = Column(String)
  amount = Column(Float)
  description = Column(String)
  source_account = Column(String)
  destination_account = Column(String)
  created_at = Column(DateTime, default=datetime.datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.datetime.utcnow)
  created_by = Column(Integer, ForeignKey("users.user_id"))
  updated_by = Column(Integer, ForeignKey("users.user_id"))
  created_by_user = relationship("Users", foreign_keys=[created_by], back_populates="created_loan_transactions")
  updated_by_user = relationship("Users", foreign_keys=[updated_by], back_populates="updated_loan_transactions")
  loan_application = relationship("Loan_applications", back_populates="loan_transactions")

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime


class Loan_applications(Base):
    __tablename__ = "loan_applications"
    loan_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    member_id = Column(Integer, ForeignKey("members.member_id"))
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
    loan_transactions = relationship("Loan_transactions", back_populates="loan_applications")
    members = relationship("Members", back_populates="loan_applications")
    created_user = relationship("Users", foreign_keys=[created_by], back_populates="loan_applications_created")
    updated_user = relationship("Users", foreign_keys=[updated_by], back_populates="loan_applications_updated")

class Loan_transactions(Base):
  __tablename__ = "loan_transactions"
  transaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  loan_id = Column(Integer, ForeignKey("loan_applications.loan_id"))
  transaction_type = Column(String)
  amount = Column(Float)
  description = Column(String)
  source_account = Column(String)
  destination_account = Column(String)
  related_document = Column(String)
  created_at = Column(DateTime, default=datetime.datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.datetime.utcnow)
  created_by = Column(Integer, ForeignKey("users.user_id"))
  updated_by = Column(Integer, ForeignKey("users.user_id"))
  loan_applications = relationship("Loan_applications", back_populates="loan_transactions")
  created_user = relationship("Users", foreign_keys=[created_by], back_populates="loan_transactions_created")
  updated_user = relationship("Users", foreign_keys=[updated_by], back_populates="loan_transactions_updated")

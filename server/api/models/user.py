from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime
from .member import Members
from .loan import Loan_applications, Loan_transactions
from .ekub import Ekub_applications
from .share import Share_applications, Share_prices, Share_transactions
class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    firstname = Column(String(100))
    lastname = Column(String(100))
    hashed_password = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(100), unique=True, index=True)
    role = Column(String(100))
    status = Column(Boolean, default=True)
    photo = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    members = relationship("Members", back_populates="users")
    loan_applications = relationship("Loan_applications", back_populates="users")
    loan_transactions = relationship("Loan_transactions", back_populates="users")
    ekub_applications = relationship("Ekub_applications",back_populates= "users")
    ekub_members = relationship("Ekub_members", back_populates="users")
    ekub_transactions = relationship("Ekub_transactions", back_populates="users")
    share_applications = relationship("Share_applications", back_populates="users")
    share_prices = relationship("Share_prices", back_populates="users")
    share_transactions = relationship("Share_transactions", back_populates="users")

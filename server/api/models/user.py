from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime
from .member import Members
from .loan import Loan_applications, Loan_transactions
from .ekub import Ekub_applications
from .share import Share_applications, Share_prices, Share_transactions
from .saving import Saving_applications, Saving_transactions
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
    user_status = Column(String, default="active")
    photo = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    members_created = relationship("Members", foreign_keys="[Members.created_by]", back_populates="created_user")
    members_updated = relationship("Members", foreign_keys="[Members.updated_by]", back_populates="updated_user")
    loan_applications_created = relationship("Loan_applications", foreign_keys="[Loan_applications.created_by]", back_populates="created_user")
    loan_applications_updated = relationship("Loan_applications", foreign_keys="[Loan_applications.updated_by]", back_populates="updated_user")
    loan_transactions_created = relationship("Loan_transactions", foreign_keys="[Loan_transactions.created_by]", back_populates="created_user")
    loan_transactions_updated = relationship("Loan_transactions", foreign_keys="[Loan_transactions.updated_by]", back_populates="updated_user")
    ekub_applications_created = relationship("Ekub_applications", foreign_keys="[Ekub_applications.created_by]", back_populates="created_user")
    ekub_applications_updated = relationship("Ekub_applications", foreign_keys="[Ekub_applications.updated_by]", back_populates="updated_user")
    ekub_members_created = relationship("Ekub_members", foreign_keys="[Ekub_members.created_by]", back_populates="created_user")
    ekub_members_updated = relationship("Ekub_members", foreign_keys="[Ekub_members.updated_by]", back_populates="updated_user")
    ekub_transactions_created = relationship("Ekub_transactions", foreign_keys="[Ekub_transactions.created_by]", back_populates="created_user")
    ekub_transactions_updated = relationship("Ekub_transactions", foreign_keys="[Ekub_transactions.updated_by]", back_populates="updated_user")
    share_applications_created = relationship("Share_applications", foreign_keys="[Share_applications.created_by]", back_populates="created_user")
    share_applications_updated = relationship("Share_applications", foreign_keys="[Share_applications.updated_by]", back_populates="updated_user")
    share_prices_created = relationship("Share_prices", foreign_keys="[Share_prices.created_by]", back_populates="created_user")
    share_prices_updated = relationship("Share_prices", foreign_keys="[Share_prices.updated_by]", back_populates="updated_user")
    share_transactions_created = relationship("Share_transactions", foreign_keys="[Share_transactions.created_by]", back_populates="created_user")
    share_transactions_updated = relationship("Share_transactions", foreign_keys="[Share_transactions.updated_by]", back_populates="updated_user")
    saving_applications_created = relationship("Saving_applications", foreign_keys="[Saving_applications.created_by]", back_populates="created_user")
    saving_applications_updated = relationship("Saving_applications", foreign_keys="[Saving_applications.updated_by]", back_populates="updated_user")
    saving_transactions_created = relationship("Saving_transactions", foreign_keys="[Saving_transactions.created_by]", back_populates="created_user")
    saving_transactions_updated = relationship("Saving_transactions", foreign_keys="[Saving_transactions.updated_by]", back_populates="updated_user")


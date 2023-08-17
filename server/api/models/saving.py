from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Saving_applications(Base):
     __tablename__ = "saving_applications"
     saving_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
     member_id = Column(Integer, ForeignKey("members.member_id"))
     saving_type = Column(String)
     interest_rate = Column(Float)
     saving_status = Column(String)
     total_amount = Column(Float)
     created_at = Column(DateTime, default=datetime.datetime.utcnow)
     updated_at = Column(DateTime, default=datetime.datetime.utcnow)
     created_by = Column(Integer, ForeignKey("users.user_id"))
     updated_by = Column(Integer, ForeignKey("users.user_id"))
     members = relationship("Members", back_populates="saving_applications")
     saving_transactions = relationship("Saving_transactions", back_populates="saving_applications")
     created_user = relationship("Users", foreign_keys=[created_by], back_populates="saving_applications_created")
     updated_user = relationship("Users", foreign_keys=[updated_by], back_populates="saving_applications_updated")

class Saving_transactions(Base):
      __tablename__ = "saving_transactions"
      transaction_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
      saving_id= Column(Integer, ForeignKey("saving_applications.saving_id"))
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
      saving_applications = relationship("Saving_applications", back_populates="saving_transactions")
      created_user = relationship("Users", foreign_keys=[created_by], back_populates="saving_transactions_created")
      updated_user = relationship("Users", foreign_keys=[updated_by], back_populates="saving_transactions_updated")

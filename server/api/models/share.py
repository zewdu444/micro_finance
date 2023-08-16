from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Share_applications(Base):
     __tablename__ = "share_applications"
     share_holder_id = Column(Integer, primary_key=True, index=True)
     member_id = Column(Integer, ForeignKey('members.member_id'))
     share_type = Column(String)
     shares_owned = Column(Float)
     total_shares_value = Column(Float)
     share_status = Column(String)
     created_at = Column(DateTime, default=datetime.datetime.utcnow)
     updated_at = Column(DateTime, default=datetime.datetime.utcnow)
     members = relationship("Members", back_populates="share_applications")
     users = relationship("User", back_populates="share_applications")
     share_transactions = relationship("Share_transactions", back_populates="share_applications")

class Share_prices(Base):
    __tablename__ = "share_prices"
    share_price_id = Column(Integer, primary_key=True, index=True)
    share_type = Column(String)
    price = Column(Float)
    reason= Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.user_id"))
    updated_by = Column(Integer, ForeignKey("users.user_id"))
    users = relationship("User", back_populates="share_prices")

class Share_transactions(Base):
      __tablename__ = "share_transactions"
      transaction_id = Column(Integer, primary_key=True, index=True)
      share_holder_id = Column(Integer, ForeignKey("share_applications.share_holder_id"))
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
      share_applications = relationship("share_applications", back_populates="share_transactions")
      users = relationship("Users", back_populates="share_transactions")




from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Ekub_applications(Base):
     __tablename__ = "ekub_applications"
     ekub_id = Column(Integer, primary_key=True, index=True)
     group_name = Column(String, index=True)
     group_leader = Column(Integer, ForeignKey("members.member_id"))
     rotation_type = Column(String)
     total_amount_received = Column(Float)
     total_amount_paid = Column(Float)
     start_date = Column(DateTime)
     end_date = Column(DateTime)
     group_size = Column(Integer)
     related_document = Column(String)
     ekub_status = Column(String)
     is_completed = Column(Boolean)
     location = Column(String)
     description = Column(String)
     current_distribution_order = Column(Integer)
     created_at = Column(DateTime, default=datetime.datetime.utcnow)
     updated_at = Column(DateTime, default=datetime.datetime.utcnow)
     created_by = Column(Integer, ForeignKey("users.user_id"))
     updated_by = Column(Integer, ForeignKey("users.user_id"))
     members = relationship("Members", back_populates="ekub_applications")
     users = relationship("Users", back_populates="ekub_applications")
     ekub_members = relationship("Ekub_members", back_populates="ekub_applications")
class Ekub_members(Base):
      __tablename__ = "ekub_members"
      ekub_member_id = Column(Integer, primary_key=True, index=True)
      ekub_id = Column(Integer, ForeignKey("ekub_applications.ekub_id"))
      member_id = Column(Integer, ForeignKey("members.member_id"))
      ekub_member_status = Column(String)
      amount_paid = Column(Float)
      amount_received = Column(Float)
      amount_remaining = Column(Float)
      distribution_order = Column(Integer)
      created_at = Column(DateTime, default=datetime.datetime.utcnow)
      updated_at = Column(DateTime, default=datetime.datetime.utcnow)
      created_by = Column(Integer, ForeignKey("users.user_id"))
      updated_by = Column(Integer, ForeignKey("users.user_id"))
      ekub_applications = relationship("Ekub_applications", back_populates="ekub_members")
      members = relationship("Members", back_populates="ekub_members")
      users = relationship("Users", back_populates="ekub_members")
      ekub_transactions = relationship("Ekub_transactions", back_populates="ekub_members")
class Ekub_transactions(Base):
      __tablename__ = "ekub_transactions"
      transaction_id = Column(Integer, primary_key=True, index=True)
      ekub_member_id = Column(Integer, ForeignKey("ekub_members.ekub_member_id"))
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
      ekub_members = relationship("Ekub_members", back_populates="ekub_transactions")
      users = relationship("Users", back_populates="ekub_transactions")
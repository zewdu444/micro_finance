from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime
class Members(Base):
    __tablename__ = "members"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String(100))
    middlename = Column(String(100))
    lastname = Column(String(100))
    country = Column(String(100))
    city = Column(String(100))
    sub_city = Column(String(100))
    wereda = Column(String(100))
    kebele = Column(String(100))
    gender = Column(String(100))
    birth_date = Column(DateTime)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(100), unique=True, index=True)
    photo = Column(String)
    employment_status = Column(String(100))
    marital_status = Column(String(100))
    emergency_contact_name = Column(String(100))
    emergency_contact_phone = Column(String(100))
    emergency_contact_relation = Column(String(100))
    is_currently_borrowed = Column(Boolean, default=False)
    borrowed_bank = Column(String(100))
    ekub_member =Column(Boolean, default=True)
    loan_member =Column(Boolean, default=True)
    insurance_member =Column(Boolean, default=True)
    commission_member =Column(Boolean, default=True)
    share_member =Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    created_by_user = relationship("Users", foreign_keys=[created_by], back_populates="created_members")
    updated_by_user = relationship("Users", foreign_keys=[updated_by], back_populates="updated_members")
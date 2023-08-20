from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
import datetime
from .user import User
class Gender(str, Enum):
    male = "male"
    female = "female"
class EmploymentStatus(str, Enum):
    employed = "employed"
    unemployed = "unemployed"
    self_employed = "self_employed"
class MaritalStatus(str, Enum):
    single = "single"
    married = "married"
    divorced = "divorced"
    widowed = "widowed"

class MemberCreate(BaseModel):
   firstname: str = Field(..., example="Zewdu")
   middlename : str = Field(..., example="Erkyhun")
   lastname : str = Field(..., example="Anley")
   country : str = Field(..., example="Ethiopia")
   city: str = Field (...,example="Addis Ababa")
   sub_city: str = Field (..., example="addis ketema")
   wereda: str = Field(..., example="08")
   kebele :str =Field(..., example="12")
   gender : Gender = Field(..., example="male")
   birth_date : datetime.datetime = Field(...)
   email: EmailStr = Field(..., example="zewdu444@gmail.com")
   phone: str = Field(..., example="+251911223344")
   employment_status : EmploymentStatus = Field(..., example="employed")
   marital_status : MaritalStatus = Field(..., example="single")
   emergency_contact_name: str = Field(...,example="minilik")
   emergency_contact_phone: str = Field(...,example="+251911223344")
   emergency_contact_relation: str = Field(...,example="brother")
   is_currently_borrowed: bool = Field(...,example=True)
   borrowed_bank: str = Field(...,example="CBE")
   ekub_member: bool = Field(...,example=True)
   loan_member: bool = Field(...,example=True)
   insurance_member: bool = Field(...,example=True)
   commission_member: bool = Field(...,example=True)
   share_member: bool = Field(...,example=True)
class MemberUpdate(BaseModel):
   firstname: Optional[str] = Field(None, example="Zewdu")
   middlename : Optional[str] = Field(None, example="Erkyhun")
   lastname : Optional[str] = Field(None, example="Anley")
   country : Optional[str]= Field(None, example="Ethiopia")
   city: Optional[str] = Field (None,example="Addis Ababa")
   sub_city: Optional[str] = Field (None, example="addis ketema")
   wereda: Optional[str] = Field(None, example="08")
   kebele :Optional[str] =Field(None, example="12")
   gender : Optional[Gender] = Field(None, example="male")
   birth_date :Optional[datetime.datetime] = Field(None, example="1998-01-01")
   email: Optional[EmailStr] = Field(None, example="zewdu444@gmail.com")
   phone: Optional[str] = Field(None, example="+251911223344")
   employment_status :Optional[EmploymentStatus] = Field(None, example="employed")
   marital_status : Optional[MaritalStatus]= Field(None, example="single")
   emergency_contact_name: Optional[str] = Field(None,example="minilik")
   emergency_contact_phone: Optional[str] = Field(None,example="+251911223344")
   emergency_contact_relation: Optional[str] = Field(None,example="brother")
   is_currently_borrowed: Optional[bool] = Field(None,example=True)
   borrowed_bank: Optional[str] = Field(None,example="CBE")
   ekub_member: Optional[bool] = Field(None,example=True)
   loan_member: Optional[bool] = Field(None,example=True)
   insurance_member: Optional[bool] = Field(None,example=True)
   commission_member: Optional[bool] = Field(None,example=True)
   share_member: Optional[bool] = Field(None,example=True)
class Member(BaseModel):
   member_id: int = Field(..., example=1)
   firstname: str = Field(..., example="Zewdu")
   middlename : str = Field(..., example="Erkyhun")
   lastname : str = Field(..., example="Anley")
   country : str = Field(..., example="Ethiopia")
   city: str = Field (...,example="Addis Ababa")
   sub_city: str = Field (..., example="addis ketema")
   wereda: str = Field(..., example="08")
   kebele :str =Field(..., example="12")
   gender : Gender = Field(..., example="male")
   birth_date : datetime.datetime = Field(...)
   email: EmailStr = Field(..., example="zewdu444@gmail.com")
   phone: str = Field(..., example="+251911223344")
   photo: Optional[str] = Field(None, example="www.example.jpg")
   employment_status : EmploymentStatus = Field(..., example="employed")
   marital_status : MaritalStatus = Field(..., example="single")
   emergency_contact_name: str = Field(...,example="minilik")
   emergency_contact_phone: str = Field(...,example="+251911223344")
   emergency_contact_relation: str = Field(...,example="brother")
   is_currently_borrowed: bool = Field(...,example=True)
   borrowed_bank: str = Field(...,example="CBE")
   ekub_member: bool = Field(...,example=True)
   loan_member: bool = Field(...,example=True)
   insurance_member: bool = Field(...,example=True)
   commission_member: bool = Field(...,example=True)
   share_member: bool = Field(...,example=True)
   created_at: datetime.datetime = Field(...)
   updated_at: datetime.datetime = Field(...)
   created_by: User
   updated_by: User

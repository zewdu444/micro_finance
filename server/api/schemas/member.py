from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
import datetime

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
   firtname: str = Field(..., example="Zewdu")
   middlename : str = Field(..., example="Erkyhun")
   lastname : str = Field(..., example="Anley")
   country : str = Field(..., example="Ethiopia")
   city: str = Field (...,examples="Addis Ababa")
   sub_city: str = Field (..., examples="addis ketema")
   wereda: str = Field(..., examples="08")
   kebele :str =Field(..., examples="12")
   gender : Gender = Field(..., examples="male")
   birth_date : datetime.datetime = Field(...)
   email: EmailStr = Field(..., example="zewdu444@gmail.com")
   phone: str = Field(..., example="+251911223344")
   photo: Optional[str] = Field(None, example="www.example.jpg")
   employment_status : EmploymentStatus = Field(..., examples="employed")
   marital_status : MaritalStatus = Field(..., examples="single")
   emergency_contact_name: str = Field(...,examples="minilik")
   emergency_contact_phone: str = Field(...,examples="+251911223344")
   emergency_contact_relation: str = Field(...,examples="brother")
   is_currently_employed: bool = Field(...,examples=True)
   borrowed_bank: str = Field(...,examples="CBE")
   ekub_member: bool = Field(...,examples=True)
   loan_member: bool = Field(...,examples=True)
   insurance_member: bool = Field(...,examples=True)
   commission_member: bool = Field(...,examples=True)
   share_member: bool = Field(...,examples=True)
   created_at: datetime.datetime = Field(...)
   updated_at: datetime.datetime = Field(...)

class MemberUpdate(BaseModel):
   firtname: Optional[str] = Field(None, example="Zewdu")
   middlename : Optional[str] = Field(None, example="Erkyhun")
   lastname : Optional[str] = Field(None, example="Anley")
   country : Optional[str]= Field(None, example="Ethiopia")
   city: Optional[str] = Field (None,examples="Addis Ababa")
   sub_city: Optional[str] = Field (None, examples="addis ketema")
   wereda: Optional[str] = Field(None, examples="08")
   kebele :Optional[str] =Field(None, examples="12")
   gender : Optional[Gender] = Field(None, examples="male")
   birth_date :Optional[datetime.datetime] = Field(None, examples="1998-01-01")
   email: Optional[EmailStr] = Field(None, example="zewdu444@gmail.com")
   phone: Optional[str] = Field(None, example="+251911223344")
   photo: Optional[str] = Field(None, example="www.example.jpg")
   employment_status :Optional[EmploymentStatus] = Field(None, examples="employed")
   marital_status : Optional[MaritalStatus]= Field(None, examples="single")
   emergency_contact_name: Optional[str] = Field(None,examples="minilik")
   emergency_contact_phone: Optional[str] = Field(None,examples="+251911223344")
   emergency_contact_relation: Optional[str] = Field(None,examples="brother")
   is_currently_employed: Optional[bool] = Field(None,examples=True)
   borrowed_bank: Optional[str] = Field(None,examples="CBE")
   ekub_member: Optional[bool] = Field(None,examples=True)
   loan_member: Optional[bool] = Field(None,examples=True)
   insurance_member: Optional[bool] = Field(None,examples=True)
   commission_member: Optional[bool] = Field(None,examples=True)
   share_member: Optional[bool] = Field(None,examples=True)
   updated_at: datetime.datetime = Field(...)

class Member(BaseModel):
   id: int = Field(..., example=1)
   firtname: str = Field(..., example="Zewdu")
   middlename : str = Field(..., example="Erkyhun")
   lastname : str = Field(..., example="Anley")
   country : str = Field(..., example="Ethiopia")
   city: str = Field (...,examples="Addis Ababa")
   sub_city: str = Field (..., examples="addis ketema")
   wereda: str = Field(..., examples="08")
   kebele :str =Field(..., examples="12")
   gender : Gender = Field(..., examples="male")
   birth_date : datetime.datetime = Field(...)
   email: EmailStr = Field(..., example="zewdu444@gmail.com")
   phone: str = Field(..., example="+251911223344")
   photo: Optional[str] = Field(None, example="www.example.jpg")
   employment_status : EmploymentStatus = Field(..., examples="employed")
   marital_status : MaritalStatus = Field(..., examples="single")
   emergency_contact_name: str = Field(...,examples="minilik")
   emergency_contact_phone: str = Field(...,examples="+251911223344")
   emergency_contact_relation: str = Field(...,examples="brother")
   is_currently_employed: bool = Field(...,examples=True)
   borrowed_bank: str = Field(...,examples="CBE")
   ekub_member: bool = Field(...,examples=True)
   loan_member: bool = Field(...,examples=True)
   insurance_member: bool = Field(...,examples=True)
   commission_member: bool = Field(...,examples=True)
   share_member: bool = Field(...,examples=True)
   created_at: datetime.datetime = Field(...)
   updated_at: datetime.datetime = Field(...)
   user_id: int = Field(..., example=1)

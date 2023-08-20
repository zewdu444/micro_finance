from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
import schemas.member as Member_schemas
import models.member as Member_models
import models.user as User_models
from database import get_db, engine
from sqlalchemy.orm import Session, Query
from sqlalchemy import  or_
import datetime
import os
import shutil
import uuid
from typing import Optional
from .auth import get_current_user, get_user_exception
from utils.fileupload import store_picture
from sqlalchemy_filters import apply_filters, apply_sort, apply_pagination
router = APIRouter(prefix="/members", tags=["members"], responses={404: {"description": "Not found"}})
Member_models.Base.metadata.create_all(bind=engine)

#  get all members
@router.get("/", response_model=list[Member_schemas.Member])
async def get_members(db: Session = Depends(get_db),
                      login_user:dict=Depends(get_current_user),
                      search: Optional[str] = None,
                      marital_status: Optional[str] = None,
                      employment_status: Optional[str] = None,
                      gender : Optional[str] = None,
                      sort_by: Optional[str] = None,
                      page_number: Optional[int] = 1,
                      page_size: Optional[int] = 10):
    if login_user is None:
        raise get_user_exception
    query :Query = db.query(Member_models.Members)
    # search
    if search:
        search_term = f"%{search}%"
        search_fields = [
           {
            'or': [
                {'field':'firstname', 'op':'ilike', 'value':search_term},
                {'field':'middlename', 'op':'ilike', 'value':search_term},
                {'field':'lastname', 'op':'ilike', 'value':search_term},
                {'field':'email','op':'ilike', 'value':search_term},
                {'field':'phone','op':'ilike', 'value':search_term},
                {'field':'emergency_contact_name','op':'ilike', 'value':search_term},
                {'field':'emergency_contact_phone','op':'ilike', 'value':search_term},
                {'field':'emergency_contact_relation','op':'ilike', 'value':search_term},
                {'field':'city','op':'ilike', 'value':search_term},
                {'field':'sub_city','op':'ilike', 'value':search_term},
                {'field':'wereda','op':'ilike', 'value':search_term},
                {'field':'kebele','op':'ilike', 'value':search_term},
                {'field':'country','op':'ilike', 'value':search_term},

            ],
           }
        ]
        query = apply_filters(query, search_fields, search_term)
    # filter by field
    if marital_status:
        marital_status_filter = [{'field':'marital_status', 'op': '==', 'value': marital_status}, ]
        query = apply_filters(query, marital_status_filter, marital_status)
    if employment_status:
        employment_status_filter = [{'field':'employment_status', 'op': '==', 'value': employment_status}, ]
        query = apply_filters(query, employment_status_filter, employment_status)
    if gender:
        gender_filter = [{'field':'gender', 'op':'==', 'value':gender}]
        query =apply_filters(query,gender_filter,gender)
    # order by
    if sort_by:
        sorted_by_fields = [{'field': sort_by, 'direction': 'asc'}]
        query = apply_sort(query, sorted_by_fields)
    # pagination
    query, pagination = apply_pagination(query, page_number=page_number, page_size=page_size)
    if len(query.all()) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No members found")
    members = query.all()
    # update member created_user and updated_user
    for member in members:
        member.created_by = db.query(User_models.Users).filter(User_models.Users.user_id == member.created_by).first()
        member.updated_by = db.query(User_models.Users).filter(User_models.Users.user_id == member.updated_by).first()
    return members

# get member by id

@router.get("/{id}", response_model=Member_schemas.Member)
async def get_member(id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    member = db.query(Member_models.Members).filter(Member_models.Members.member_id == id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Member with id {id} not found")
    member.created_by = db.query(User_models.Users).filter(User_models.Users.user_id == member.created_by).first()
    member.updated_by = db.query(User_models.Users).filter(User_models.Users.user_id == member.updated_by).first()
    return member
# create new member
@router.post("/")
async def create_member(member: Member_schemas.MemberCreate, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
   if login_user is None:
      raise get_user_exception
   find_member = db.query(Member_models.Members).filter(Member_models.Members.email == member.email).first() or db.query(Member_models.Members).filter(Member_models.Members.phone == member.phone).first()
   if find_member:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Member already exists")
   else:
     new_member=Member_models.Members(**member.dict())
     new_member.updated_at = datetime.datetime.now()
     new_member.created_at = datetime.datetime.now()
     new_member.created_by = login_user.user_id
     new_member.updated_by = login_user.user_id
     db.add(new_member)
     db.commit()
     db.refresh(new_member)
     return {"message": "Member created successfully"}

 # update member
@router.put("/{id}")
async def update_member(id:int, member:Member_schemas.MemberUpdate, db:Session=Depends(get_db),login_user:dict =Depends(get_current_user)):
     if login_user is None:
         raise get_user_exception
     member_update = db.query(Member_models.Members).filter(Member_models.Members.member_id == id).first()
     if member_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"member with id {id} not found")
     else:
        for key, value in member.dict(exclude_unset=True).items():
                setattr(member_update, key, value)
        member_update.updated_at =datetime.datetime.now()
        member_update.updated_by =login_user.user_id
        db.commit()
        return {"message":"Member updated successfully"}
# delete member
@router.delete("/{id}")
async def delete_member(id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
         raise get_user_exception
    member_delete = db.query(Member_models.Members).filter(Member_models.Members.member_id == id).first()
    if member_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"member with id {id} not found")
    else:
        db.delete(member_delete)
        db.commit()
        return  {"message": "Member deleted successfully"}

# upload profile picture
@router.put("/uploadprofile/{id}}")
async def upload_profile_image(id:int, login_user:dict=Depends(get_current_user), file: UploadFile = File(...), db: Session = Depends(get_db)):
     if login_user is None:
         raise get_user_exception
     if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
         raise HTTPException(status_code=400, detail="File must be an image")
     member_update_picture = db.query(Member_models.Members).filter(Member_models.Members.member_id == id).first()
     if member_update_picture is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"member with id {id} not found")
     else:
        member_update_picture.photo = store_picture(file,"../uploads/profile/")
        member_update_picture.updated_at =datetime.datetime.utcnow()
        member_update_picture.updated_by =login_user.user_id
        db.commit()
     return {"message": "Profile image uploaded successfully"}

#  delete profile picture
@router.delete("/deleteprofile/{id}")
async def delete_profile_image(id:int, login_user:dict=Depends(get_current_user), db: Session = Depends(get_db)):
        if login_user is None:
            raise get_user_exception
        member_delete_picture = db.query(Member_models.Members).filter(Member_models.Members.member_id == id).first()
        if member_delete_picture is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"member with id {id} not found")
        else:
            member_delete_picture.photo = None
            member_delete_picture.updated_at =datetime.datetime.utcnow()
            member_delete_picture.updated_by =login_user.user_id
            db.commit()
            return {"message": "Profile image deleted successfully"}

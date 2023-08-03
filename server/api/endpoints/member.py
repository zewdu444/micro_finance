from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
import schemas.member as Member_schemas
import models.member as Member_models
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
router = APIRouter(prefix="/members", tags=["members"], responses={404: {"description": "Not found"}})
Member_models.Base.metadata.create_all(bind=engine)

#  get all members
@router.get("/", response_model=list[Member_schemas.Member])
async def get_members(db: Session = Depends(get_db),
                       login_user:dict=Depends(get_current_user),
                      search: Optional[str] = None,
                      filter_field: Optional[str] = None,
                      order_by: Optional[str] = None,
                      order_desc: Optional[bool] = False):
    if login_user is None:
        raise get_user_exception
    query :Query = db.query(Member_models.Members)
    # search
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(Member_models.Members.firstname.ilike(search_term),
                Member_models.Members.lastname.ilike(search_term),
                Member_models.Members.email.ilike(search_term),
                Member_models.Members.phone.ilike(search_term),
                )
                )
        try:
            date_search = datetime.datetime.strptime(search, "%Y-%m-%d")
            query = query.filter(
                or_(
                    Member_models.Members.created_at >= date_search,
                    Member_models.Members.updated_at >= date_search,
                ))
        except ValueError:
            pass
     # filter by field
    if filter_field:
        if filter_field == "gender":
            query = query.filter(Member_models.Members.role == "male") or query.filter(Member_models.Members.role == "female")
        elif filter_field == "marital_status":
            query = query.filter(Member_models.Members.marital_status == "single")
    # order by
    if order_by:
        column_attr = getattr(Member_models.Members, order_by, None)
        if column_attr is not None:
            if order_desc:
                 query = query.order_by(column_attr.desc())
            else:
                query = query.order_by(column_attr.asc())
    members = query.all()
    return members

# get member by id

@router.get("/{id}", response_model=Member_schemas.Member)
async def get_member(id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    member = db.query(Member_models.Members).filter(Member_models.Members.id == id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Member with id {id} not found")
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
     new_member.created_by = login_user.id
     new_member.updated_by = login_user.id
     db.add(new_member)
     db.commit()
     db.refresh(new_member)
     return {"message": "Member created successfully"}

 # update member
@router.put("/{id}")
async def update_member(id:int, member:Member_schemas.MemberUpdate, db:Session=Depends(get_db),login_user:dict =Depends(get_current_user)):
     if login_user is None:
         raise get_user_exception
     member_update = db.query(Member_models.Members).filter(Member_models.Members.id == id).first()
     if member_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"member with id {id} not found")
     else:
        for key, value in member.dict(exclude_unset=True).items():
                setattr(member_update, key, value)
        member_update.updated_at =datetime.datetime.now()
        member_update.updated_by =login_user.id
        db.commit()
        return {"message":"Member updated successfully"}
# delete member
@router.delete("/{id}")
async def delete_member(id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
         raise get_user_exception
    member_delete = db.query(Member_models.Members).filter(Member_models.Members.id == id).first()
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
     member_update_picture = db.query(Member_models.Members).filter(Member_models.Members.id == id).first()
     if member_update_picture is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"member with id {id} not found")
     else:
        member_update_picture.photo = store_picture(file,"../uploads")
        member_update_picture.updated_at =datetime.datetime.utcnow()
        member_update_picture.updated_by =login_user.id
        db.commit()
     return {"message": "Profile image uploaded successfully"}

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
import schemas.user as schemas
import models.user as models
from database import get_db, engine
from sqlalchemy.orm import Session, Query
from sqlalchemy import  or_
import datetime
from utils.fileupload import store_picture
from typing import Optional
from .auth import get_current_user, get_user_exception
from sqlalchemy_filters import apply_filters, apply_sort, apply_pagination
router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})

models.Base.metadata.create_all(bind=engine)

@router.post("/checking_filter", response_model=list[schemas.User])
async def checking_filter(db: Session = Depends(get_db),
                           login_user:dict=Depends(get_current_user),
                           search: Optional[str] = None,
                           role: Optional[str] = None,
                           staus: Optional[str] = None,
                           order_by: Optional[str] = None):
    if login_user is None:
        raise get_user_exception
    query :Query = db.query(models.Users)
    # search by field
    if search:
        search_term = f"%{search}%"
        search_fields = [
           {
            'or': [
                {'field':'username', 'op':'ilike', 'value':search_term},
                {'field': 'firstname', 'op': 'ilike', 'value': search_term},
                {'field':'lastname', 'op': 'ilike', 'value': search_term},
                {'field':'email','op':'ilike', 'value':search_term},
                {'field':'phone','op':'ilike', 'value':search_term},
            ],

           }
        ]
        query = apply_filters(query, search_fields, search_term)
    # filter by field
    if role:
        role_filter = [{'field':'role', 'op': '==', 'value': role}, ]
        query = apply_filters(query, role_filter, role)
    if staus:
        status_filter = [{'field':'status', 'op': '==', 'value': staus}, ]
        query = apply_filters(query, status_filter, staus)
    # order by
    if order_by:
        order_by_fields = ["firstname", "lastname", "email", "phone", "role"]
        query = apply_sort(query, order_by_fields, order_by)
    return query.all()

# get all users
@router.get("/", response_model=list[schemas.User])
async def get_users(db: Session = Depends(get_db),
    login_user:dict=Depends(get_current_user),
    search: Optional[str] = None,
    filter_field: Optional[str] = None,
    order_by: Optional[str] = None,
    order_desc: Optional[bool] = False):
    if login_user is None:
        raise get_user_exception
    query :Query = db.query(models.Users)
    # search
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(models.Users.firstname.ilike(search_term),
                models.Users.lastname.ilike(search_term),
                models.Users.email.ilike(search_term),
                models.Users.phone.ilike(search_term),
                models.Users.role.ilike(search_term),
                )
                )
        try:
            date_search = datetime.datetime.strptime(search, "%Y-%m-%d")
            query = query.filter(
                or_(
                    models.Users.created_at >= date_search,
                    models.Users.updated_at >= date_search,
                ))
        except ValueError:
            pass  # The search term is not a valid date, so we ignore it for date columns
    # filter by field
    if filter_field:
        if filter_field == "role":
            query = query.filter(models.Users.role == "admin")
        elif filter_field == "status":
            query = query.filter(models.Users.status == "active")
    # order by
    if order_by:
        column_attr = getattr(models.Users, order_by, None)
        if column_attr is not None:
            if order_desc:
                 query = query.order_by(column_attr.desc())
            else:
                 query = query.order_by(column_attr.asc())

    users = query.all()
    return users

# get user by id
@router.get("/{id}", response_model=schemas.User)
async def get_user(id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise http_exception(status.HTTP_404_NOT_FOUND, f"User with id {id} not found")
    else:
        return user

# update user by id
@router.put("/{id}")
async def update_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
     if login_user is None:
        raise get_user_exception
     user_update = db.query(models.Users).filter(models.Users.id == id).first()
     if user_update is None:
          raise http_exception(status.HTTP_404_NOT_FOUND, f"User with id {id} not found")
     else:
            for key, value in user.dict(exclude_unset=True).items():
                setattr(user_update, key, value)
            user_update.updated_at =datetime.datetime.utcnow()
            db.commit()
            return  {"message": "User updated successfully"}

# delete user by id
@router.delete("/{id}")
async def delete_user(id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
        if login_user is None:
            raise get_user_exception
        user_delete = db.query(models.Users).filter(models.Users.id == id).first()
        if user_delete is None:
            raise http_exception(status.HTTP_404_NOT_FOUND, f"User with id {id} not found")
        else:
                db.delete(user_delete)
                db.commit()
                return  {"message": "User deleted successfully"}

# update user photo
@router.post("/uploadprofile" )
async def upload_profile_image(user:dict=Depends(get_current_user), file: UploadFile = File(...), db: Session = Depends(get_db)):
     if user is None:
         raise get_user_exception
     if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
         raise HTTPException(status_code=400, detail="File must be an image")
     login_user =db.query(models.Users).filter(models.Users.username==user.username).first()
     login_user.photo = store_picture(file,"../uploads")
     login_user.updated_at =datetime.datetime.utcnow()
     db.add(login_user)
     db.commit()
     return {"message": "Profile image uploaded successfully"}

def http_exception(status_code, detail):
    raise HTTPException(status_code=status_code, detail=detail)


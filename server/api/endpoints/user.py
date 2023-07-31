from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
import schemas.user as schemas
import models.user as models
from database import get_db, engine
from sqlalchemy.orm import Session
import datetime
import os
import shutil
import uuid
from .auth import get_current_user, get_user_exception
router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})

models.Base.metadata.create_all(bind=engine)


# get all users
@router.get("/", response_model=list[schemas.User])
async def get_users(db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    users = db.query(models.User).all()
    return users
# get user by id
@router.get("/{id}", response_model=schemas.User)
async def get_user(id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
    if login_user is None:
        raise get_user_exception
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise http_exception(status.HTTP_404_NOT_FOUND, f"User with id {id} not found")
    else:
        return user

# update user by id
@router.put("/{id}")
async def update_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
     if login_user is None:
        raise get_user_exception
     user_update = db.query(models.User).filter(models.User.id == id).first()
     if user_update is None:
          raise http_exception(status.HTTP_404_NOT_FOUND, f"User with id {id} not found")
     else:
            user_update.firstname = user.firstname
            user_update.lastname = user.lastname
            user_update.email = user.email
            user_update.phone = user.phone
            user_update.role = user.role
            user_update.photo = user.photo
            user_update.updated_at =datetime.datetime.utcnow()
            db.add(user_update)
            db.commit()
            return  {"message": "User updated successfully"}

# delete user by id
@router.delete("/{id}")
async def delete_user(id: int, db: Session = Depends(get_db), login_user:dict=Depends(get_current_user)):
        if login_user is None:
            raise get_user_exception
        user_delete = db.query(models.User).filter(models.User.id == id).first()
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
     login_user =db.query(models.User).filter(models.User.username==user.username).first()
     login_user.photo = store_picture(file)
     login_user.updated_at =datetime.datetime.utcnow()
     db.add(login_user)
     db.commit()
     return {"message": "Profile image uploaded successfully"}

def http_exception(status_code, detail):
    raise HTTPException(status_code=status_code, detail=detail)

def store_picture(file):
    upload_folder = os.path.join(os.getcwd(), "../uploads")
    if not os.path.exists(upload_folder):
        os.mkdir(upload_folder)
    #get destination path
    dest = os.path.join(upload_folder, f"{uuid.uuid1(clock_seq=1)}{file.filename}")
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return dest


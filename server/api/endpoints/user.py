from fastapi import APIRouter, Depends, HTTPException, status
import schemas.user as schemas
import models.user as models
from database import get_db, engine
from sqlalchemy.orm import Session
import datetime
from .auth import get_current_user, get_user_exception
router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})

models.Base.metadata.create_all(bind=engine)


# get all users
@router.get("/", response_model=list[schemas.User])
async def get_users(db: Session = Depends(get_db), user:dict=Depends(get_current_user)):
    if user is None:
        raise get_user_exception
    users = db.query(models.User).all()
    return users

# get user by id
@router.get("/{id}", response_model=schemas.User)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise http_exception(status.HTTP_404_NOT_FOUND, f"User with id {id} not found")
    else:
        return user

# update user by id
@router.put("/{id}")
async def update_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
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
async def delete_user(id: int, db: Session = Depends(get_db)):
        user_delete = db.query(models.User).filter(models.User.id == id).first()
        if user_delete is None:
            raise http_exception(status.HTTP_404_NOT_FOUND, f"User with id {id} not found")
        else:
                db.delete(user_delete)
                db.commit()
                return  {"message": "User deleted successfully"}

def http_exception(status_code, detail):
    raise HTTPException(status_code=status_code, detail=detail)

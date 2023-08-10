
from fastapi import APIRouter, Depends, HTTPException, status
import schemas.user as schemas
import models.user as models
from database import get_db, engine
from sqlalchemy.orm import Session
from .auth  import get_password_hash
import datetime
from .auth import create_access_token
from pathlib import Path
router = APIRouter(tags=["password management"], responses={404: {"description": "Not found"}})
models.Base.metadata.create_all(bind=engine)


@router.post("/send_email")


@router.put("/resetpassword")
async def reset_password(user: schemas.UserResetPassword, db: Session = Depends(get_db)):
  find_user = db.query(models.Users).filter(models.Users.email == user.email).first() or db.query(models.Users).filter(models.Users.username == user.username).first()
  if find_user is None:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
  if user.password != user.confirm_password:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
  find_user.hashed_password = get_password_hash(user.password)
  find_user.updated_at = datetime.datetime.utcnow()
  db.add(find_user)
  db.commit()
  return {"message": "Password reset successfully"}

@router.post("/send_forget_password_email")
def send_forget_passowrd_email():
    return {"message":"send forget password email "}

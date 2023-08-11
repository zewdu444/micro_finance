
from fastapi import APIRouter, Depends, HTTPException, status,Query
import schemas.user as schemas
import models.user as models
from database import get_db, engine
from sqlalchemy.orm import Session
from .auth  import get_password_hash
from jose import JWTError, jwt
import datetime
from .auth import create_access_token
from pathlib import Path
from utils.email import password_request_mail
from schemas.email import PasswordRequestSchema
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
router = APIRouter(tags=["password management"], responses={404: {"description": "Not found"}})
models.Base.metadata.create_all(bind=engine)

SECRET_KEY = SECRET_KEY
ALGORITHM = ALGORITHM

@router.post("/send_reset_email")
async def send_reset_email(email:str, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    #  generate token
    token = create_access_token(data={"email": email}, expires_delta=datetime.timedelta(minutes=30))
    #  send email
    password_request_data = {
    "email": ["zewdu.erkyhun@yandex.com"],
    "subject": "Password Reset Request",
    "body": {
        "data": {
            "username": user.username,
            "title": "Password Reset Request",
            "message": "You're receiving this email because you requested a password reset for your account.",
            "message_below": "If you didn't request a password reset you can safely ignore this email.",
            "link": "http://localhost:8000/resetpassword?token="+token,
        }
       }
    }
    try:
        await password_request_mail(PasswordRequestSchema(**password_request_data))
        return {"message": "Email has been sent please check your email"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email could not be sent")


@router.put("/resetpassword")
async def reset_password(user: schemas.UserResetPassword, token:str =Query(..., description="The reset token provided in the reset link "), db: Session = Depends(get_db)):
  request_user_email =decode_user(token)
  request_user = db.query(models.Users).filter(models.Users.email == request_user_email).first()
  if request_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
  if user.password != user.confirm_password:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
  request_user.hashed_password = get_password_hash(user.password)
  request_user.updated_at = datetime.datetime.utcnow()
  db.add(request_user)
  db.commit()
  return {"message": "Password reset successful"}

def decode_user(user_token:str):
    try:
        payload = jwt.decode(user_token, SECRET_KEY, algorithms=ALGORITHM)
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

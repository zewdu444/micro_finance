
from fastapi import APIRouter, Depends, HTTPException, status
import schemas.user as schemas
import models.user as models
from database import get_db, engine
from sqlalchemy.orm import Session
from .auth  import get_password_hash
import datetime
from .auth import create_access_token
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
router = APIRouter(tags=["password management"], responses={404: {"description": "Not found"}})
models.Base.metadata.create_all(bind=engine)

conf = ConnectionConfig(
    MAIL_USERNAME = "zewdu.anley@email.com",
    MAIL_PASSWORD = "0013B5526C23A34E9E3107BD101D1B6DBF0D",
    MAIL_FROM = "zewdu444@gmail.com",
    MAIL_PORT = 2525,
    MAIL_SERVER = "smtp.elasticemail.com",
    MAIL_FROM_NAME="Zewdu Anley",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,

)

@router.post("/send_email")
async  def simple_send():
    html ="""<p>Hi this test mail, thanks for using Fastapi-mail</p> """
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients= ["arrow9941519zewdu@gmail.com","zewdu.erkyhun@yandex.com"],
        body=html,
        subtype=MessageType.html)
    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "sent"}

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

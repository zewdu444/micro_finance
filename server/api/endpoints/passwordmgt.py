
from fastapi import APIRouter, Depends, HTTPException, status
import schemas.user as schemas
import models.user as models
from database import get_db, engine
from sqlalchemy.orm import Session
from .auth  import get_password_hash
import datetime
router = APIRouter(tags=["password management"], responses={404: {"description": "Not found"}})
models.Base.metadata.create_all(bind=engine)

@router.put("/resetpassword")
async def reset_password(user: schemas.UserResetPassword, db: Session = Depends(get_db)):
  find_user = db.query(models.User).filter(models.User.email == user.email).first() or db.query(models.User).filter(models.User.username == user.username).first()
  if find_user is None:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
  if user.password != user.confirm_password:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
  find_user.hashed_password = get_password_hash(user.password)
  find_user.updated_at = datetime.datetime.utcnow()
  db.add(find_user)
  db.commit()
  return {"message": "Password reset successfully"}

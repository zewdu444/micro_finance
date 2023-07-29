from fastapi import APIRouter, Depends, HTTPException, status
import schemas.user as schemas
import models.user as models
from database import get_db, engine
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})

models.Base.metadata.create_all(bind=engine)

# create user
@router.post("/")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, firstname=user.firstname, lastname=user.lastname, email=user.email, phone=user.phone, role=user.role, photo=user.photo, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully"}


# get all users
@router.get("/", response_model=list[schemas.User])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

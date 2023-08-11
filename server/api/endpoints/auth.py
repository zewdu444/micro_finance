from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from passlib.context import CryptContext
import schemas.user as schemas
import models.user as models
from database import get_db, engine
from sqlalchemy.orm import Session
from typing import Optional
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
router = APIRouter(prefix="/users", tags=["auth"], responses={404: {"description": "Not found"}})
models.Base.metadata.create_all(bind=engine)
# sectet key
SECRET_KEY = SECRET_KEY
ALGORITHM = ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES

# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
      return pwd_context.hash(password)

# authenticate user
def authenticate_user(db: Session, username: str, password: str):
      user = db.query(models.Users).filter(models.Users.username == username).first()
      if not user:
          return False
      if not verify_password(password, user.hashed_password):
          return False
      return user


# create jwt token
def create_access_token(data:dict, expires_delta:timedelta | None =None):
     to_encode=data.copy()
     if expires_delta:
        expire =datetime.utcnow() + expires_delta
     else:
        expire =datetime.utcnow() + timedelta(minutes=15)
     to_encode.update({'exp' :expire})
     encode_jwt =jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
     return encode_jwt

# get current user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
   try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      username: str = payload.get("username")
      if username is None:
         raise get_user_exception()
      current_user = db.query(models.Users).filter(models.Users.username == username).first()
      if current_user is None:
         raise get_user_exception()
      return current_user
   except JWTError:
      raise get_user_exception()

@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
      user = authenticate_user(db, form_data.username, form_data.password)
      if not user:
         raise get_login_exception()
      access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      access_token = create_access_token(data={"username": user.username}, expires_delta=access_token_expires)
      return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def  user_registration(user: schemas.UserCreate, db: Session = Depends(get_db)):
      find_user = db.query(models.Users).filter(models.Users.email == user.email).first()
      if find_user:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
      else:
        db_user = models.Users(username=user.username, firstname=user.firstname, lastname=user.lastname, email=user.email, phone=user.phone, role=user.role, photo=user.photo, hashed_password=get_password_hash(user.hashed_password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User created successfully"}

# exception handling
def get_user_exception():
   return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

def get_login_exception():
   return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

from pydantic import BaseModel
from model import Users
from fastapi import APIRouter,Depends,HTTPException,Path
from Database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from datetime import timedelta,datetime,timezone



router=APIRouter(
    perfix='/auth',
    tags=['auth']
)

SECRET_KEY= '5860762474adae5c17fff27201b6be9cbae43bf94ed59216cac4132e181a0094'
AlGORITHM="HS256"

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl="auth/token")



class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str

class Token(BaseModel):
    access_token:str
    token_type:str

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

def authenticate_user(username:str,password:str,db):
    user=db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

def create_access_token(username:str,user_id:int,expires_delta:timedelta):

    encode={'sub':username,"id":user_id}
    expires=datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=AlGORITHM)

async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[AlGORITHM])
        username:str=payload.get('sub')
        user_id:int=payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        return {'username':username,'id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user.")



@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request:CreateUserRequest):
    create_user_model=Users(
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()

@router.post("/token",response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user=authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    token=create_access_token(user.username,user.id,timedelta(minutes=20))
    return {'access_token':token, "token_type":"bearer"}

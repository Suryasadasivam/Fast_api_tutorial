from fastapi import APIRouter,Depends,HTTPException,Path
from Database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from model import todo,Users
from pydantic import BaseModel,Field
from .auth import get_current_user
from passlib.context import CryptContext


from starlette import status

router=APIRouter(
    prefix='/user',
    tags=['user']
)



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

@router.get('/',status_code=status.HTTP_200_OK)
async def user_info(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    return db.query(Users).filter(Users.id==user.get('id')).first()
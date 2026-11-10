from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from starlette import status
from database import SessionLocal
from user_verification import UserVerification
from users import Users
from .auth import get_current_user

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[SessionLocal, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def get_current_active_user(
        user: user_dependency,
        db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication fails')
    users = db.query(Users).filter(user.get('id') == Users.id).first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return users

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(
        user: user_dependency,
        db: db_dependency,
        user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication fails!')
    user_model = db.query(Users).filter(user.get('id') == Users.id).first()
    user_verified = bcrypt_context.verify(user_verification.password, user_model.hashed_password)
    if not user_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error on password fails!')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
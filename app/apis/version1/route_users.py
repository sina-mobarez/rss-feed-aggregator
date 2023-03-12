from typing import List
from fastapi import APIRouter, status
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from schemas.users import UserCreate, ShowUser
from db.session import get_db
from db.repository.users import create_new_user, get_users_list, get_user_by_id
from core.otp import username_is_unique, phone_number_is_unique, email_is_unique

router = APIRouter()


@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if not username_is_unique(user.username, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"username is already in used")
    elif not email_is_unique(user.email, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"email is already in used")
    elif not phone_number_is_unique(user.phone_number, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"phonenumber is already in used")
    user = create_new_user(user=user, db=db)
    return user


@router.get('/', response_model=List[ShowUser])
def get_users(db: Session = Depends(get_db)):
    users = get_users_list(db=db)
    return users


@router.get('/{pk}', response_model=ShowUser)
def get_user(pk: int, db: Session = Depends(get_db)):
    user = get_user_by_id(pk, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user not found")
    return user

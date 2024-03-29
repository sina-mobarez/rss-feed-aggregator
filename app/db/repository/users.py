from fastapi import Depends, HTTPException, status
import jwt
from db.session import get_db
from schemas.token import TokenData
from core.config import settings
from sqlalchemy.orm import Session
from datetime import datetime
from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher
from core.otp import generate_key
from core.jwt import config_set_jwt_token_to_head
import pyotp


def create_new_user(user: UserCreate, db: Session):
    user = User(username=user.username,
                email=user.email,
                hashed_password=Hasher.get_password_hash(user.password),
                phone_number=user.phone_number,
                is_active=True,
                is_superuser=False,
                date_registered=datetime.now().strftime("%Y-%m-%d"),
                otp_key=generate_key(db)
                )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_users_list(db: Session):
    users = db.query(User).all()
    return users


def get_user_by_id(pk, db: Session):
    user = db.query(User).filter(User.id == pk).first()
    if not user:
        return False
    return user


def get_user_by_username_phone_number_email(username_or_phone_number_or_email, db: Session):
    get_user_phone_number = db.query(User).filter(
        User.phone_number == username_or_phone_number_or_email).first()
    get_user_email = db.query(User).filter(User.email == username_or_phone_number_or_email).first()
    get_user_username = db.query(User).filter(User.username == username_or_phone_number_or_email).first()
    if (get_user_email or get_user_phone_number or get_user_username) is not None:
        if get_user_email is not None:
            return get_user_email
        elif get_user_phone_number is not None:
            return get_user_phone_number
        elif get_user_username is not None:
            return get_user_username
    else:
        return False


def authenticate_user(username_or_phone_number_or_email: str, password: str, db: Session):
    user = get_user_by_username_phone_number_email(username_or_phone_number_or_email=username_or_phone_number_or_email, db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


def authenticate_otp_code(user: User, code: int):
    try:
        provided_otp = int(code)
    except:
        return False
    otp = pyotp.TOTP(user.otp_key, interval=300)
    return otp.verify(provided_otp)


def get_current_user(token: str = Depends(config_set_jwt_token_to_head)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        upe: str = payload.get("sub")
        if upe is None:
            raise credentials_exception
        token_data = TokenData(username=upe)
    except Exception:
        raise credentials_exception
    db = next(get_db())
    user = get_user_by_username_phone_number_email(
        username_or_phone_number_or_email=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active == False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

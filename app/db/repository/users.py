from sqlalchemy.orm import Session
from datetime import datetime
from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher
from core.otp import generate_key
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


def get_user_by_username_phone_number_email(upe, db: Session):
    get_user_phone_number = db.query(User).filter(
        User.phone_number == upe).first()
    get_user_email = db.query(User).filter(User.email == upe).first()
    get_user_username = db.query(User).filter(User.username == upe).first()
    if (get_user_email or get_user_phone_number or get_user_username) is not None:
        if get_user_email is not None:
            return get_user_email
        elif get_user_phone_number is not None:
            return get_user_phone_number
        elif get_user_username is not None:
            return get_user_username
    else:
        return False


def authenticate_user(upe: str, password: str, db: Session):
    user = get_user_by_username_phone_number_email(upe=upe, db=db)
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

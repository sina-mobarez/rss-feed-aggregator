from sqlalchemy.orm import Session
from datetime import datetime
from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher
from core.otp import generate_key


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
    return user
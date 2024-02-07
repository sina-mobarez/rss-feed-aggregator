from sqlalchemy import Column, String, Boolean, DateTime
from db.base import Base


class User(Base):
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=True, unique=True)
    phone_number = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    is_verified = Column(Boolean(), default=False)
    date_registered = Column(DateTime)
    otp_key = Column(String, nullable=False, unique=True)


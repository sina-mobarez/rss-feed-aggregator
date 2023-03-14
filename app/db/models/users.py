from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=True, unique=True, index=True)
    phone_number = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    is_verified = Column(Boolean(), default=False)
    date_registered = Column(DateTime)
    otp_key = Column(String, nullable=False, unique=True)


# owner_id =  Column(Integer,ForeignKey("user.id"))
# owner = relationship("User",back_populates="jobs")

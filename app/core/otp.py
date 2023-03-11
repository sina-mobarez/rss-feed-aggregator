import pyotp
from db.models.users import User



def generate_key(db):
    key = pyotp.random_base32()
    if is_unique(key, db):
        return key
    generate_key(db)


def is_unique(key, db):
    user = db.query(User).filter(User.otp_key == key).first()
    if not user:
        return True
    return False

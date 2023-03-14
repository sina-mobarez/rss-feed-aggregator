import pyotp
from db.models.users import User
from ippanel import Client
from core.config import settings


def generate_key(db):
    key = pyotp.random_base32()
    if key_is_unique(key, db):
        return key
    generate_key(db)


def key_is_unique(key, db):
    user = db.query(User).filter(User.otp_key == key).first()
    if not user:
        return True
    return False


def phone_number_is_unique(phone_number, db):
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        return True
    return False


def username_is_unique(username, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return True
    return False


def email_is_unique(email, db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return True
    return False


def send_sms(receptor, code):
    sms = Client(settings.SEND_SMS_API_KEY)
    pattern_value = {'verification-code': f"{code}"}
    try:
        sms.send_pattern(settings.SEND_SMS_PATTERN_KEY,
                         settings.SEND_SMS_SENDER_NUMBER, receptor, pattern_value)
        return True
    except Exception:
        return False

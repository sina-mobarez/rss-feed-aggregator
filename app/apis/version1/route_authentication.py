
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends, HTTPException
from db.session import get_db
from db.repository.users import authenticate_user, get_user_by_username_phone_number_email, authenticate_otp_code
from core.otp import send_sms
import pyotp
from schemas.users import Message, SendCodeOTP, ShowUser, VerifyCodeOTP
from schemas.token import Token
from fastapi.security import OAuth2PasswordRequestForm
from core.jwt import create_access_token, create_refresh_token


router = APIRouter()


@router.post("/send-code-to-phone-number/", response_model=Message, status_code=status.HTTP_200_OK)
def send_code_to_phone_number(username_or_phone_number_or_email: SendCodeOTP, db: Session = Depends(get_db)):
    user = get_user_by_username_phone_number_email(username_or_phone_number_or_email=username_or_phone_number_or_email, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user not found")
    code = pyotp.TOTP(user.otp_key, interval=300).now()
    sms = send_sms(user.phone_number, code)
    if not sms:
        return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                             detail=f"sms service unavailable for now")
    return {'message': 'done!'}


@router.post("/verify-phone-numer/", response_model=ShowUser, status_code=status.HTTP_202_ACCEPTED)
def verify_phone_number(username_or_phone_number_or_email: VerifyCodeOTP, db: Session = Depends(get_db)):
    user = get_user_by_username_phone_number_email(username_or_phone_number_or_email=username_or_phone_number_or_email, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user not found")
    verify = authenticate_otp_code(user=user, code=username_or_phone_number_or_email.code)
    if not verify:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"verification code is wrong")
    user.is_verified = True
    db.commit()
    return user


@router.post('/get-jwt-token/', summary="Create access and refresh tokens for user", response_model=Token)
def create_jwt_tokens(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(username_or_phone_number_or_email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email/username/phone-number or password"
        )

    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }

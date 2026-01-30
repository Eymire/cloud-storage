from fastapi import APIRouter
from fastapi.security import HTTPBearer
from pydantic import EmailStr

from src.dependencies import current_user_access_dep, current_user_refresh_dep, session_dep
from src.schemas.auth import SignIn as SignInSchema
from src.schemas.auth import SignUp as SignUpSchema
from src.schemas.auth import Token as TokenSchema
from src.schemas.auth import VerifyOTP as VerifyOTPSchema
from src.schemas.users import UserProfile as UserProfileSchema

from . import services


router = APIRouter()


@router.post('/sign_up')
async def sign_up(
    session: session_dep,
    data: SignUpSchema,
):
    await services.sign_up(
        session,
        data,
    )


@router.post('/verify_otp')
async def verify_otp(
    session: session_dep,
    data: VerifyOTPSchema,
) -> TokenSchema:
    result = await services.verify_otp(
        session,
        data,
    )

    return result  # type: ignore[return-value]


@router.post('/resend_otp')
async def resend_otp(
    session: session_dep,
    email: EmailStr,
):
    await services.resend_otp(
        session,
        email,
    )


@router.post('/sign_in')
async def sign_in(
    session: session_dep,
    data: SignInSchema,
) -> TokenSchema:
    result = await services.sign_in(
        session,
        data,
    )

    return result  # type: ignore[return-value]


security = HTTPBearer()


@router.post('/refresh')
async def refresh(
    current_user: current_user_refresh_dep,
    session: session_dep,
) -> TokenSchema:
    result = await services.refresh(
        session,
        current_user.id,
    )

    return result  # type: ignore[return-value]


@router.get('')
async def get_current_user(
    current_user: current_user_access_dep,
) -> UserProfileSchema:
    return current_user  # type: ignore[return-value]

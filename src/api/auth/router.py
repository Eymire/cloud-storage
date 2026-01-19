from fastapi import APIRouter

from src.dependencies import current_user_access_dep, session_dep

from . import services
from .schemas import SignInSchema, SignUpSchema, TokenSchema, UserProfileSchema


router = APIRouter()


@router.post('/sign_up')
async def sign_up(
    session: session_dep,
    data: SignUpSchema,
) -> TokenSchema:
    result = await services.sign_up(
        session,
        data,
    )

    return result  # type: ignore[return-value]


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


@router.get('')
async def get_current_user(
    current_user: current_user_access_dep,
) -> UserProfileSchema:
    return current_user  # type: ignore[return-value]

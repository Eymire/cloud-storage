import hashlib
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import delete, insert, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import PendingUser as PendingUserModel
from src.models import User as UserModel
from src.schemas.auth import SignIn as SignInSchema
from src.schemas.auth import SignUp as SignUpSchema
from src.schemas.auth import VerifyOTP as VerifyOTPSchema
from src.settings import auth_settings

from .dependencies import (
    create_access_token,
    create_refresh_token,
    generate_otp,
    hash_password,
    send_otp_email,
    verify_password,
)


async def sign_up(
    session: AsyncSession,
    data: SignUpSchema,
):
    stmt = select(UserModel).where(
        or_(
            UserModel.name == data.name,
            UserModel.email == data.email,
        )
    )
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()

    if result:
        conflict_field = 'name' if result.name == data.name else 'email'
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User with this {conflict_field} already exists.',
        )

    # TODO: Спитатись в левесв про цей момент
    stmt = delete(PendingUserModel).where(
        or_(
            PendingUserModel.name == data.name,
            PendingUserModel.email == data.email,
        )
    )
    await session.execute(stmt)

    otp = generate_otp()
    otp_hash = hashlib.sha256(otp.encode()).hexdigest()
    expires_at = datetime.now(UTC) + timedelta(minutes=auth_settings.otp_expire_minutes)

    stmt = insert(PendingUserModel).values(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        otp_hash=otp_hash,
        expires_at=expires_at,
    )
    await session.execute(stmt)
    await session.commit()

    await send_otp_email(data.email, otp)


async def verify_otp(
    session: AsyncSession,
    data: VerifyOTPSchema,
):
    stmt = select(PendingUserModel).where(PendingUserModel.email == data.email)
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Registration not found. Please sign up again.',
        )

    if datetime.now(UTC) > result.expires_at:
        stmt = delete(PendingUserModel).where(PendingUserModel.id == result.id)
        await session.execute(stmt)
        await session.commit()
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail='OTP code expired. Sign up again.',
        )

    otp_hash = hashlib.sha256(data.otp.encode()).hexdigest()
    if otp_hash != result.otp_hash:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid OTP code.',
        )

    stmt = (
        insert(UserModel)
        .values(
            name=result.name,
            email=result.email,
            password_hash=result.password_hash,
        )
        .returning(UserModel.id)
    )
    result = await session.execute(stmt)
    result = result.scalar_one()

    stmt = delete(PendingUserModel).where(PendingUserModel.id == result)
    await session.execute(stmt)
    await session.commit()

    return {
        'access_token': create_access_token(result),
        'refresh_token': await create_refresh_token(result, session),
    }


async def resend_otp(
    session: AsyncSession,
    email: str,
):
    stmt = select(PendingUserModel).where(PendingUserModel.email == email)
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Registration not found. Please sign up again.',
        )

    otp = generate_otp()
    otp_hash = hashlib.sha256(otp.encode()).hexdigest()
    expires_at = datetime.now(UTC) + timedelta(minutes=auth_settings.otp_expire_minutes)

    stmt = (
        update(PendingUserModel)
        .where(PendingUserModel.id == result.id)
        .values(otp_hash=otp_hash, expires_at=expires_at)
    )
    await session.execute(stmt)
    await session.commit()

    await send_otp_email(email, otp)


async def sign_in(
    session: AsyncSession,
    data: SignInSchema,
) -> dict:
    stmt = select(UserModel).where(UserModel.name == data.name)
    result = await session.execute(stmt)
    result = result.scalar_one_or_none()

    if not result or not verify_password(data.password, result.password_hash):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.',
        )

    return {
        'access_token': create_access_token(result.id),
        'refresh_token': await create_refresh_token(result.id, session),
    }


async def refresh(
    session: AsyncSession,
    user_id: int,
) -> dict:
    return {
        'access_token': create_access_token(user_id),
        'refresh_token': await create_refresh_token(user_id, session),
    }

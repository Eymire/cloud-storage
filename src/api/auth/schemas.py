from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class SignInSchema(BaseModel):
    name: str = Field(min_length=4, max_length=32)
    password: str = Field(min_length=8)


class SignUpSchema(BaseModel):
    name: str = Field(min_length=4, max_length=32)
    email: EmailStr
    password: str = Field(min_length=8)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'


class UserProfileSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='APP_',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    environment: Literal['development', 'production'] = 'development'
    root_path: str | None = None


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='DB_',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    host: str
    name: str
    user: str
    password: str


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='AUTH_',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    jwt_access_lifetime_minutes: int
    jwt_refresh_lifetime_minutes: int
    otp_expire_minutes: int


class SMTPSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='SMTP_',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    host: str
    port: int
    user: str
    password: str


app_settings = AppSettings()  # type: ignore[call-arg]
db_settings = DatabaseSettings()  # type: ignore[call-arg]
auth_settings = AuthSettings()  # type: ignore[call-arg]
smtp_settings = SMTPSettings()  # type: ignore[call-arg]

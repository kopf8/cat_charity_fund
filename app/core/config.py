from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'QRkot'
    app_description: str = 'Приложение для Благотворительного фонда поддержки котиков QRKot'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    jwt_token_lifetime: int = 3600
    user_password_min_len: int = 4
    logging_format: str = '%(asctime)s - %(levelname)s - %(message)s'
    logging_dt_format: str = '%Y-%m-%d %H:%M:%S'

    class Config:
        env_file = '.env'


settings = Settings()


class Constants:
    JWT_TOKEN_URL = 'auth/jwt/login'
    JWT_AUTH_BACKEND_NAME = 'jwt'
    NAME_MIN_LEN = 1
    NAME_MAX_LEN = 100
    PROJECT_ENDPOINTS_PREFIX = '/charity_project'
    PROJECT_ENDPOINTS_TAGS = ('charity_projects',)
    DONATION_ENDPOINTS_PREFIX = '/donation'
    DONATION_ENDPOINTS_TAGS = ('donations',)


class Messages:
    PASSWORD_TOO_SHORT = (
        f'Password should be at least {settings.user_password_min_len} '
        'characters long'
    )
    EMAIL_IN_PASSWORD = 'Password should not contain email'
    USER_REGISTERED = 'User registered: '
    INVESTMENT_ERROR = 'An error has occurred during investment'
    PROJECT_AMOUNTS_ERROR = 'Full amount cannot be less than already invested amount'
    PROJECT_FUTURE_DATE_ERROR = 'Date of project opening cannot be in the future'
    PROJECT_NAME_OCCUPIED = 'Project name already occupied'
    PROJECT_NAME_NOT_NULL = 'Project name cannot be empty'
    PROJECT_DESCRIPTION_NOT_NULL = 'Project description cannot be empty'
    PROJECT_NOT_FOUND = 'Project with given ID not found'
    PROJECT_INVESTED = 'Project was already invested, cannot delete'
    PROJECT_CLOSED = 'Closed project cannot be edited'

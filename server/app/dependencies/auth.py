from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.config.settings import jwt_settings
from app.crud.users import user as user_crud
from app.dependencies.session import CookieAuth
from app.models.users import Users
from app.schemas.users import TokenData

oauth2_scheme = CookieAuth(token_url="/api/login")

SECRET_KEY = jwt_settings.secret_key
ALGORITHM = jwt_settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = jwt_settings.token_expires


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


async def get_current_user(
    header_token: Annotated[Optional[str], Depends(oauth2_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(header_token, credentials_exception)
    return await user_crud.get_one(token.id)


def get_current_active_user(
    current_user: Users = Depends(get_current_user),
) -> Users:
    if not user_crud.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: Users = Depends(get_current_user),
) -> Users:
    if not user_crud.is_admin(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

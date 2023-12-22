import json
from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from redis.asyncio import Redis
from starlette.responses import RedirectResponse

from app.config.settings import app_settings, jwt_settings
from app.crud.users import user
from app.dependencies.auth import create_access_token, get_current_user
from app.dependencies.crypt import verify
from app.dependencies.session import init_redis_client
from app.models.users import Users
from app.schemas.users import UserBase

router = APIRouter(tags=["Authentication"], prefix="/api")
logger: structlog.stdlib.BoundLogger = structlog.getLogger(__name__)


@router.post("/login", response_class=RedirectResponse)
async def login(
    request: Request,
    # FIXME: We don't want to "init_redis_client" this every time
    redis: Annotated[Redis, Depends(init_redis_client)],
    user_credentials: OAuth2PasswordRequestForm = Depends(),
):
    auth_user = await user.get_by_email(user_credentials.username)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Credentials",
        )

    if not verify(user_credentials.password, auth_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Credentials",
        )

    request.session["user_id"] = str(auth_user.id)
    return RedirectResponse(
        request.url_for("dashboard"), status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="token", domain=app_settings.url_base)
    return response


@router.get("/authenticated", response_model=UserBase)
def read_user_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/forgot/password", response_model=UserBase)
def forgot_password(req: Request):
    body = req.query_params
    email = body.get("email", None)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Must give email"
        )

    forgotten_user = user.get_by_email(email=email)
    if not forgotten_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"User not found"
        )

    return forgotten_user.__dict__


@router.get("/update/password")
def update_password(current_user: Users = Depends(get_current_user)):
    pass

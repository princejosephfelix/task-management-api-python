from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.core.security import decode_access_token
from app.database.database import get_db
from app.database.models import User, UserRole
from app.auth.repository import UserRepository


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    try:
        payload = decode_access_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, TypeError, ValueError):
        raise AppException(401, "Invalid or expired token", "invalid_token")

    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise AppException(401, "User no longer exists", "invalid_user")

    return user


def require_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise AppException(403, "Administrator role required", "forbidden")
    return current_user

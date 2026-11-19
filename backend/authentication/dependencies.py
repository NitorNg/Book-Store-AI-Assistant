"""current_user: add `user: dict = Depends(current_user)` to any route that needs login."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from . import service

_bearer = HTTPBearer()


def current_user(cred: HTTPAuthorizationCredentials = Depends(_bearer)) -> dict:
    """
    Verifies the token Casdoor issued and returns its claims, e.g.
    {"sub": "<casdoor user id>", "name": "...", "email": "...", "displayName": "...", ...}
    """
    try:
        return service.verify_token(cred.credentials)
    except Exception:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
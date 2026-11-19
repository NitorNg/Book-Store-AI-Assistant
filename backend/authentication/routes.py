
"""The /auth endpoints: register, login, me."""
from fastapi import APIRouter, Depends, HTTPException, status
 
from . import service
from .dependencies import current_user
from .schemas import LoginIn, RegisterIn, TokenOut
 
router = APIRouter(prefix="/auth", tags=["auth"])
 
 
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: RegisterIn):
    if service.username_taken(body.username):
        raise HTTPException(status.HTTP_409_CONFLICT, "Username is already taken")
    if service.find_username(body.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email is already registered")
 
    try:
        service.create_user(body.username, body.email, body.password)
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Could not register: {e}")
 
    return {"message": "Registered successfully"}
 
 
@router.post("/login", response_model=TokenOut)
def login(body: LoginIn):
    username = service.find_username(body.email)
    if not username:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
 
    token = service.get_token(username, body.password)
    if "access_token" not in token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
 
    return TokenOut(
        access_token=token["access_token"],
        refresh_token=token.get("refresh_token"),
    )
 
 
@router.get("/me")
def me(user: dict = Depends(current_user)):
    return {
        "id": user.get("sub"),
        "username": user.get("name"),
        "email": user.get("email"),
        "display_name": user.get("displayName"),
    }
 
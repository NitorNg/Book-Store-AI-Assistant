
"""The /auth endpoints: register, login, me."""
from fastapi import APIRouter, Depends, HTTPException, status
 
from . import service
from .dependencies import current_user
from .schemas import LoginIn, RegisterIn, TokenOut
from sqlalchemy.orm import Session
from database import get_db
from .users import create_local_user
import logging

router = APIRouter(prefix="/auth", tags=["auth"])
 
# logger is basically like print info to the terminal.
logger = logging.getLogger(__name__)

# This endpoint handles user creation in both casdoor and fastapi.
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: RegisterIn, db: Session = Depends(get_db)):
    if service.username_taken(body.username):
        raise HTTPException(status.HTTP_409_CONFLICT, "Username is already taken")
    if service.find_username(body.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email is already registered")
 
    # 1. Casdoor first. If it rejects the user, stop here and save nothing locally.
    try:
        casdoor_id = service.create_user(body.username, body.email, body.password)
    except Exception as e:
        raise HTTPException(400, f"Could not create user: {e}")

    # 2. Then our database. If this fails, registration still succeeds;
    #    current_db_user (Step 3) will create the row on the user's first login.
    if casdoor_id:
        try:
            create_local_user(db, casdoor_id, body.username, body.email)
        except Exception:
            db.rollback()
            try:
                service.delete_user(body.username)
            except Exception:
                logger.exception("Could not remove %s from Casdoor either", body.username)
            raise HTTPException(500, "Registration failed, please try again")
    return {"message": "User created"}
 
 
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
 
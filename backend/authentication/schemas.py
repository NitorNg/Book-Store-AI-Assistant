"""Shapes of the JSON that the auth routes accept and return."""
from pydantic import BaseModel, EmailStr, Field


class RegisterIn(BaseModel):
    # Casdoor usernames: letters, numbers, underscores, hyphens only
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_-]+$")
    email: EmailStr
    password: str = Field(min_length=6)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"
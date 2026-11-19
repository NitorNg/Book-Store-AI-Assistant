"""Lets other files keep writing: from auth import router, current_user"""
from .dependencies import current_user
from .routes import router

__all__ = ["router", "current_user"]
from casdoor import User
 
from .config import sdk
 
# summary: This file is for managing user, get user from the database.  
def username_taken(username: str) -> bool:
    """True if a user with this username already exists in our Casdoor organization."""
    try:
        user = sdk.get_user(username)
    except Exception:
        return False
    # Casdoor may answer "ok" with an empty user when nobody has this name
    return bool(user and user.name == username)
 
 
def find_username(email: str) -> str | None:
    """Return the Casdoor username that belongs to an email, or None if there is none."""
    try:
        user = sdk.get_user_by_email(email)
        return user.name or None
    except Exception:
        return None
 
 
def create_user(username: str, email: str, password: str) -> None:
    """Create a user in Casdoor. Raises an Exception if Casdoor rejects it."""
    user = User()
    user.owner = sdk.org_name
    user.name = username
    user.email = email
    user.password = password          # Casdoor hashes it; we never store it
    user.displayName = username
    user.signupApplication = sdk.application_name
    sdk.add_user(user)
 
 
def get_token(username: str, password: str) -> dict:
    """Ask Casdoor for a token. On failure Casdoor returns {"error": ...} instead."""
    return sdk.get_oauth_token(username=username, password=password)
 
 
def verify_token(token: str) -> dict:
    """Check the token's signature and return its claims. Raises if invalid or expired."""
    return sdk.parse_jwt_token(token)
 
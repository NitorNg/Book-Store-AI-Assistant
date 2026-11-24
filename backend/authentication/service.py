from casdoor import User
 
from .config import sdk
 
# summary: This file is for managing user, get user from the casdoor's database.  
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
    except Exception as e:
        print("find_username failed:", repr(e))
        return None
 
# After create user in casdoor, return the casdoor user's id.
# We need the casdoor user's id inorder to create fastapi user.
def create_user(username: str, email: str, password: str) -> str:
    """Create a user in Casdoor. Raises an Exception if Casdoor rejects it."""
    user = User()
    user.owner = sdk.org_name
    user.name = username
    user.email = email
    user.password = password          # Casdoor hashes it; we never store it
    user.displayName = username
    user.signupApplication = sdk.application_name
    sdk.add_user(user)
    return sdk.get_user(username).id
 
 
def get_token(username: str, password: str) -> dict:
    """Ask Casdoor for a token. On failure Casdoor returns {"error": ...} instead."""
    return sdk.get_oauth_token(username=username, password=password)
 
 
def verify_token(token: str) -> dict:
    """Check the token's signature and return its claims. Raises if invalid or expired."""
    return sdk.parse_jwt_token(token)

def delete_user(username: str) -> None:
    """Remove a user from Casdoor (used to undo a half-finished registration)."""
    user = sdk.get_user(username)
    if user and user.name == username:
        sdk.delete_user(user)
 
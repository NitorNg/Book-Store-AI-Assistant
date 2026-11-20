from sqlalchemy.orm import Session

from models import User

# Just a function to create user in fastapi's sqlite database.
def create_local_user(db: Session, casdoor_id: str, username: str, email: str) -> User:
    """Save a copy of a Casdoor user in our own database."""
    user = User(casdoor_id=casdoor_id, username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)   # fills in user.id and created_at from the database
    return user
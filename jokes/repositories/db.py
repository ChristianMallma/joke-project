from sqlalchemy.orm import Session
from jokes.repositories.postgres.local_session import SessionLocal


def get_db() -> Session:
    """
    Get a SQLAlchemy Session object for database operations.

    Returns:
        Session: A SQLAlchemy Session object.
    """
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

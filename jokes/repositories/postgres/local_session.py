import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()

HOST = os.getenv('HOST')
DB_NAME = os.getenv('DB_NAME')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

SQLALCHEMY_DATABASE_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}"


class SessionLocal:
    """
    SQLAlchemy Session Local Class
    """
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def __enter__(self):
        self.session = self.Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    @classmethod
    def close(cls):
        """
        Close the current SQLAlchemy session
        """
        cls.Session.close_all()

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class JokeModel(Base):
    __tablename__ = "jokes"

    id = Column(Integer, primary_key=True, index=True)
    joke_description = Column(String)

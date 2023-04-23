from pydantic import BaseModel


# Schemas
class Joke(BaseModel):
    description: str

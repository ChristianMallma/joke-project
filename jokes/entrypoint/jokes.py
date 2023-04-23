import requests

from fastapi.routing import APIRouter, HTTPException, Request
from typing import Optional

from jokes.entrypoint.schemas.joke import Joke
from jokes.repositories.postgres.local_session import SessionLocal
from jokes.services.jokes import get_random_joke_from_db, save_joke_to_db, update_joke_in_db, get_all_jokes_from_db, \
    delete_joke_from_db

router = APIRouter()


# Endpoints
@router.get("/get_joke", tags=['Joke'])
async def get_joke(type: Optional[str] = None):
    """
        Get a random joke or a joke of a specific type (Chuck or Dad).

        Args:
            type (Optional[str], optional): The type of joke to retrieve. Valid values are "Chuck" and "Dad". Defaults
            to None.
            db (Session): The db local session.

        Returns:
            dict: A dictionary containing the retrieved joke.

        Raises:
            HTTPException: If the type parameter is not valid.
    """
    try:
        if type is None:
            with SessionLocal() as db:
                joke = get_random_joke_from_db(db)
            if not joke:
                raise HTTPException(status_code=404, detail="No joke found in database.")
            return joke

        elif type.lower() == "chuck":
            response = requests.get('https://api.chucknorris.io/jokes/random')
            response.raise_for_status()
            return {"joke": response.json()["value"]}

        elif type.lower() == "dad":
            response = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
            response.raise_for_status()
            return {"joke": response.json()["joke"]}

        else:
            raise HTTPException(status_code=400, detail="The specified joke type is not valid.")

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the joke.")

    except ValueError:
        raise HTTPException(status_code=500, detail="An error occurred while parsing the joke response.")

    except KeyError:
        raise HTTPException(status_code=500, detail="An error occurred while parsing the joke response. "
                                                    "The key isn't correct or the key changed")


@router.post("/save_joke", tags=['Joke'])
async def save_joke(joke: Joke):
    """
        Save a joke in the database.

        Args:
            joke (Joke): The joke to be saved.

        Returns:
            dict: A dictionary indicating whether the joke was saved successfully.

        Raises:
            HTTPException: If an error occurs while saving the joke.
    """
    try:
        with SessionLocal() as db:
            save_joke_to_db(db, joke.description)

        return {"message": "Joke saved successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while saving the joke: {e}")


@router.put("/update_joke/{number}", tags=['Joke'])
async def update_joke(number: int, new_joke: Joke):
    """
        Update a joke in the database.

        Args:
            number (int): The id of the joke.
            new_joke (Joke): The new joke to replace the old one.

        Returns:
            dict: A dictionary indicating whether the joke was updated successfully.

        Raises:
            HTTPException: If an error occurs while updating the joke.
    """
    with SessionLocal() as db:
        joke = update_joke_in_db(db, number, new_joke.description)
    if not joke:
        raise HTTPException(status_code=404, detail=f"Joke with id {number} not found.")
    return joke


@router.get("/get_all_jokes", tags=['Joke'])
async def get_all_jokes():
    """
        Retrieve all jokes from the database.

        Returns:
            List[Joke]: A list of dict Joke objects.

        Raises:
            HTTPException: If an error occurs while retrieving the jokes.
    """
    try:
        with SessionLocal() as db:
            jokes = get_all_jokes_from_db(db)
        return jokes

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while retrieving jokes: {e}")


@router.delete("/delete_joke/{number}", tags=['Joke'])
async def delete_joke(number: int):
    """
        Delete a joke from the database.

        Args:
            number (int): The id of the joke to be deleted.

        Returns:
            dict: A dictionary indicating whether the joke was deleted successfully.

        Raises:
            HTTPException: If an error occurs while deleting the joke.
    """
    with SessionLocal() as db:
        joke = delete_joke_from_db(db, number)
    if not joke:
        raise HTTPException(status_code=404, detail=f"Joke with id {number} not found.")
    return joke

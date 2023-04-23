from random import choice
from jokes.repositories.postgres.models import JokeModel
from sqlalchemy.orm.session import Session


def get_random_joke_from_db(session: Session):
    """
        Retrieves a random joke from the database.

        Args:
            session: The local db session.

        Returns:
            dict: A dictionary containing the retrieved joke. Returns None if there are no jokes in the database.
    """
    jokes = session.query(JokeModel).all()
    if not jokes:
        return None
    joke = choice(jokes)
    return {"joke": joke.joke_description}


def save_joke_to_db(session: Session, joke_description: str):
    """
    Saves a joke to the database.

    Args:
        session (Session): The SQLAlchemy session.
        joke_description (str): The description of the joke.

    Returns:
        None
    """
    if joke_description == '':
        raise ValueError("The description cannot be blank")

    joke_model = JokeModel(joke_description=joke_description)

    session.add(joke_model)
    session.commit()


def update_joke_in_db(session: Session, joke_id, new_description):
    """
        Updates the text of a joke in the database.

        Args:
            session: The local db session.
            joke_id (int): The id of the joke.
            new_description (str): The new description for the joke.

        Returns:
            dict: A dictionary containing a message indicating whether the joke was updated successfully.
            Returns None if the joke to be updated does not exist in the database.
    """
    joke_to_update = session.query(JokeModel).filter_by(id=joke_id).first()
    if not joke_to_update:
        return None
    joke_to_update.joke_description = new_description
    session.commit()
    return {"message": f"Joke with id {joke_id} updated successfully!"}


def get_all_jokes_from_db(session: Session):
    """
        Retrieves all jokes from the database.

        Args:
            session: The local db session.

        Returns:
            list: A list containing all the jokes in the database. Each joke is a dictionary with keys "id" and
            "description".
    """
    jokes = session.query(JokeModel).order_by(JokeModel.id).all()
    jokes = [{"id": joke.id, "description": joke.joke_description} for joke in jokes]

    return jokes


def delete_joke_from_db(session: Session, joke_id):
    """
        Deletes a joke from the database.

        Args:
            session: The local db session.
            joke_id (int): The id of the joke to be deleted.

        Returns:
            dict: A dictionary containing a message indicating whether the joke was deleted successfully.
            Returns None if the joke to be deleted does not exist in the database.
    """
    joke_to_delete = session.query(JokeModel).filter_by(id=joke_id).first()
    if not joke_to_delete:
        return None

    session.delete(joke_to_delete)
    session.commit()
    return {"message": f"Joke with id {joke_id} deleted successfully!"}

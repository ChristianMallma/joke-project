
from unittest import TestCase
from faker import Faker

from jokes.repositories.db import get_db
from jokes.repositories.postgres.models import JokeModel
from jokes.services.jokes import save_joke_to_db, update_joke_in_db


class TestUpdateJoke(TestCase):
    def setUp(self) -> None:
        self.fake_data = Faker()
        self.fake_joke_description = f"{self.fake_data.text()}-TEST"

    def test_update_joke(self):
        # First find a fake joke in db
        with get_db() as session:
            fake_joke_saved = session.query(JokeModel).\
                filter(JokeModel.joke_description.ilike(f'%-TEST%')).first()

        if fake_joke_saved is not None:
            # Update this fake joke
            with get_db() as session:
                update_joke_in_db(session, fake_joke_saved.id, self.fake_joke_description)

                # Get a fake joke updated
                updated_joke = session.query(JokeModel). \
                    filter(JokeModel.joke_description == self.fake_joke_description).first()

                self.assertEqual(updated_joke.joke_description, self.fake_joke_description)


from unittest import TestCase
from faker import Faker

from jokes.repositories.db import get_db
from jokes.repositories.postgres.models import JokeModel
from jokes.services.jokes import save_joke_to_db


class TestSaveJoke(TestCase):
    def setUp(self) -> None:
        self.fake_data = Faker()
        self.fake_joke_description = f"{self.fake_data.text()}-TEST"

    def test_save_joke(self):
        # Save a fake joke
        with get_db() as session:
            save_joke_to_db(session, self.fake_joke_description)

        # Get a fake joke saved
        with get_db() as session:
            saved_joke = session.query(JokeModel).\
                filter(JokeModel.joke_description == self.fake_joke_description).first()

        self.assertIsNotNone(saved_joke)
        self.assertEqual(saved_joke.joke_description, self.fake_joke_description)

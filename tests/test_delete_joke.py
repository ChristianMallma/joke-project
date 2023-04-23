
from unittest import TestCase
from faker import Faker

from jokes.repositories.db import get_db
from jokes.repositories.postgres.models import JokeModel
from jokes.services.jokes import delete_joke_from_db


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
            # Delete this fake joke
            with get_db() as session:
                delete_joke_from_db(session, fake_joke_saved.id)

                # Find a fake joke in db again
                fake_joke_deleted = session.query(JokeModel). \
                    filter(JokeModel.id == fake_joke_saved.id).first()

                self.assertIsNone(fake_joke_deleted)

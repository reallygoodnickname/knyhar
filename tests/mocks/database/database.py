from sqlalchemy import create_engine

from knyhar.database import database
from knyhar.models import Base

from knyhar.models.users import User


class MockDatabase(database.Database):
    def __init__(self):
        super().__init__("localhost", "username", "password")

    def _connect_to_database(self):
        """ Create in-memory table for tests """
        URI = "sqlite:///:memory:"

        self.engine = create_engine(URI)
        Base.metadata.create_all(self.engine)

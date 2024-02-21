import unittest

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

from knyhar.database.database import Database
from knyhar.models import Base

from knyhar.models.books import Book
from knyhar.models.users import User


class DatabaseTest(Database):
    def __init__(self):
        self.__connect_to_database()

    def __connect_to_database(self):
        """ Create in-memory table for tests """
        URI = "sqlite:///:memory:"

        self.engine = create_engine(URI)
        Base.metadata.create_all(self.engine)


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseTest()

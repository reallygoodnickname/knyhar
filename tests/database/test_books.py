import unittest

from mocks.database import database


class TestDatabaseBooks(unittest.TestCase):
    def setUp(self):
        self.books = database.MockDatabase().books

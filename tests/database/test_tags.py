import unittest

from tests.mocks.database import database


class TestDatabaseTags(unittest.TestCase):
    def setUp(self):
        self.tags = database.MockDatabase().tags

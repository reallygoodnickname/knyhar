import unittest

from knyhar.models.users import User

from tests.mocks.database import database


class TestDatabaseUsers(unittest.TestCase):
    def setUp(self):
        self.users = database.MockDatabase().users

        # Populate database with test data
        for i in range(1, 5):
            user = User(id=i, username=f"test{i}",
                        password="test", admin=False)
            self.users.add(user)

    def test_get_not_exists(self):
        """ Get user with wrong id """
        res = self.users.get(-1)

        self.assertIsNone(res)

    def test_get_exists(self):
        """ Get user that exists """

        res = self.users.get(1)

        self.assertIsInstance(res, User)

    def test_add_not_exists(self):
        """ Adding user that doesn't exist """
        user = User(id=6, username="test6", password="test", admin=False)

        res = self.users.add(user)

        self.assertTrue(res)

    def test_add_exists(self):
        """ Add user that already exists """
        user = User(id=1, username="test1", password="test", admin=False)

        res = self.users.add(user)

        self.assertFalse(res)

    def test_remove_exists(self):
        """ Remove user that exists """

        res = self.users.remove(1)
        self.assertTrue(res)

    def test_remove_doesnt_exist(self):
        """ Remove user that doesn't exist """

        res = self.users.remove(-1)
        self.assertFalse(res)

    def test_set_role(self):
        """ Set user a specific role """

        res = self.users.set_role(1, True)
        self.assertTrue(res)

        user = self.users.get(1)
        if user is not None:
            self.assertTrue(user.admin)

import unittest

from knyhar.models.users import User

from tests.mocks.database import database


class TestDatabaseUsers(unittest.TestCase):
    def setUp(self):
        self.users = database.MockDatabase().users

        # Populate database with test data
        for i in range(1, 5):
            self.users.add(User(id=i, username=f"test{i}",
                                password="test", admin=False))

    def test_set_role(self):
        """ Set user a specific role """

        res = self.users.set_role(1, True)
        self.assertTrue(res)

        user = self.users.get(1)
        if user is not None:
            self.assertTrue(user.admin)

    def test_get_user_by_name_exists(self):
        """ Get user by name that does exist """
        res = self.users.get_user_by_username("test1")

        self.assertIsInstance(res, User)

    def test_get_user_by_name_doesnt_exist(self):
        """ Try to get user that doesn't exist """
        res = self.users.get_user_by_username("test0")

        self.assertIsNone(res)

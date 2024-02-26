import unittest

from knyhar.models.tags import Tag

from tests.mocks.database import database


class TestDatabaseTags(unittest.TestCase):
    def setUp(self):
        self.tags = database.MockDatabase().tags

    def test_add_not_exists(self):
        """ Add tag that doesn't exist """
        tag = Tag(id=1, name="Fiction")

        res = self.tags.add(tag)
        self.assertTrue(res)

    def test_add_exists(self):
        """ Add tag that alrady exists """
        tag = Tag(id=2, name="Sci-Fi")
        tag_copy = Tag(id=2, name="Sci-Fi")

        self.tags.add(tag)
        res = self.tags.add(tag_copy)

        self.assertFalse(res)

    def test_remove_exists(self):
        """ Remove tag that exists """
        tag = Tag(id=3, name="Novell")

        self.tags.add(tag)
        res = self.tags.remove(3)

        self.assertTrue(res)

    def test_remove_doesnt_exist(self):
        """ Remove tag that doesn't exist """
        res = self.tags.remove(-1)

        self.assertFalse(res)

    def test_get_exists(self):
        """ Get tag that exists """
        tag = Tag(id=4, name="Horror")

        self.tags.add(tag)
        res = self.tags.get(4)

        self.assertIsInstance(res, Tag)

    def test_get_doesnt_exist(self):
        """ Get tag that doesn't exist """

        self.assertIsNone(self.tags.get(-1))

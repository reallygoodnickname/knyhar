import unittest

from database.test_database import DatabaseTest
from knyhar.models.books import Book


class TestDatabaseBooks(unittest.TestCase):
    def setUp(self):
        self.books = DatabaseTest().books

        # Populate database with test data
        for i in range(1, 5):
            book = Book(id=i, author="test", name=f"test{i}",
                        description="test", price=1.23)
            self.books.add(book)

    def test_get_exists(self):
        """ Get book from database with correct id """
        res = self.books.get(1)

        self.assertIsInstance(res, Book)

    def test_get_not_exists(self):
        """ Get book from database with incorrect id """
        res = self.books.get(-1)

        self.assertIsNone(res)

    def test_add_not_exists(self):
        """ Add book that doesn't exist """
        book = Book(id=6, name=f"test6", author="test",
                    description="test", price=1.23)

        self.assertTrue(self.books.add(book))

    def test_add_exists(self):
        """ Add book that exists """
        book = Book(id=1, name=f"test1", author="test",
                    description="test", price=1.23)

        self.assertFalse(self.books.add(book))

    def test_remove_exists(self):
        """ Remove book that exists """
        res = self.books.remove(1)

        self.assertTrue(res)

    def test_remove_doesnt_exist(self):
        """ Remove book that doesn't exist """
        res = self.books.remove(-1)

        self.assertFalse(res)

    def test_get_all_books(self):
        """ Get all books from database """
        res = self.books.get_all()

        self.assertNotEqual(len(res), 0)

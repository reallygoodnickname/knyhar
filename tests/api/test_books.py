import unittest
from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from knyhar.api.books import books_endpoint
from knyhar.knyhar import create_app
from knyhar.models.books import Book
from knyhar.models.tags import Tag

from tests.database.test_database import DatabaseTest
from tests.mocks.database.database import MockDatabase

endpoint_prefix = "/books"

mock_book_obj = Book(id=1, name="Test1", description="test", author="Test",
                     tags=[Tag(id=2, name="Sci-Fi")], price=1.00)

mock_books = [
    Book(id=1, name="Test1", description="test", author="Test",
         tags=[Tag(id=2, name="Sci-Fi")], price=1.00),
    Book(id=2, name="Test2", description="test", author="Test",
         tags=[Tag(id=1, name="Horror")], price=1.00)
]

test_book = {
    "name": "test book",
    "description": "Test book",
    "author": "test",
    "tags": ["Horror"],
    "price": 10.0
}


class TestApiBooks(unittest.TestCase):
    def setUp(self):
        self.database = MockDatabase()

        self.app = create_app(self.database, "supertest")
        self.app.include_router(books_endpoint)

        self.test_client = TestClient(self.app)

    def test_get_book_exist(self):
        """ Get book by ID that exists """
        self.database.books.get = MagicMock(return_value=mock_book_obj)

        response = self.test_client.get(endpoint_prefix + "/1")

        self.assertEqual(response.status_code, 200)

    def test_get_book_doesnt_exist(self):
        """ Try to get book by ID that doesn't exist """
        self.database.books.get = MagicMock(return_value=None)

        response = self.test_client.get(endpoint_prefix + "/1")

        self.assertEqual(response.status_code, 400)

    def test_get_all_books(self):
        """ Get all books from DB """
        self.database.books.get_all = MagicMock(return_value=mock_books)

        response = self.test_client.get(endpoint_prefix + "/")

        self.assertEqual(response.status_code, 200)

    def test_add_book_exists(self):
        """ Try to add book that already exists """
        self.database.books.add = MagicMock(return_value=False)

        response = self.test_client.post(endpoint_prefix + "/", json=test_book)

        self.assertEqual(response.status_code, 400)

    def test_add_book_doesnt_exist(self):
        """ Add book that doesn't exist """
        self.database.books.add = MagicMock(return_value=True)

        response = self.test_client.post(endpoint_prefix + "/", json=test_book)

        self.assertEqual(response.status_code, 200)

    def test_delete_book_exists(self):
        """ Delete book that exists """
        self.database.books.remove = MagicMock(return_value=True)

        response = self.test_client.delete(endpoint_prefix + "/1")

        self.assertEqual(response.status_code, 200)

    def test_delete_book_doesnt_exist(self):
        """ Try to delete book that doesn't exist """
        self.database.books.remove = MagicMock(return_value=False)

        response = self.test_client.delete(endpoint_prefix + "/1")

        self.assertEqual(response.status_code, 400)

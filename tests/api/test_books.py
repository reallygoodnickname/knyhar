from unittest.mock import MagicMock

from knyhar.models.books import Book
from knyhar.models.tags import Tag

from tests.api import ApiTests

endpoint_prefix = "/books"

mock_book_obj = Book(id=1, name="Test1", description="test", author="Test",
                     tags=[Tag(name="Sci-Fi")], price=1.00)

mock_books = [
    Book(id=1, name="Test1", description="test", author="Test",
         tags=[Tag(name="Sci-Fi")], price=1.00),
    Book(id=2, name="Test2", description="test", author="Test",
         tags=[Tag(name="Horror")], price=1.00)
]

test_book = {
    "name": "test book",
    "description": "Test book",
    "author": "test",
    "tags": [],
    "price": 10.0
}


class TestApiBooks(ApiTests):
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

    def test_add_book_tag_exists(self):
        """ Add book with tag that exists in database """
        book = test_book.copy()
        book["tags"] = ["Horror"]

        self.database.books.add = MagicMock(return_value=True)
        self.database.tags.get = MagicMock(return_value=Tag(name="Horror"))

        response = self.test_client.post(endpoint_prefix + "/", json=book)
        self.assertEqual(response.status_code, 200)

    def test_add_book_tag_doesnt_exist(self):
        """ Add book with tag that exists in database """
        book = test_book.copy()
        book["tags"] = ["Horror"]

        self.database.books.add = MagicMock(return_value=True)
        self.database.tags.get = MagicMock(return_value=None)

        response = self.test_client.post(endpoint_prefix + "/", json=book)
        self.assertEqual(response.status_code, 400)

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

import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from knyhar.api.books import books_endpoint

endpoint_prefix = "/books"


class TestApiBooks(unittest.TestCase):
    def setUp(self):
        self.app = FastAPI()
        self.app.include_router(books_endpoint)
        self.test_client = TestClient(self.app)

    def test_get_books(self):
        response = self.test_client.get(endpoint_prefix + "/")
        self.skipTest("Not implemented!")

    def test_add_book(self):
        test_book = {
            "name": "test book",
            "description": "Test book",
            "author": ["You"],
            "genre": ["Horror"],
            "price": 10.0
        }

        response = self.test_client.post(endpoint_prefix + "/", json=test_book)
        self.skipTest("Not implemented!")

    def test_delete_book(self):
        response = self.test_client.delete(endpoint_prefix + "/")
        self.skipTest("Not implemented!")

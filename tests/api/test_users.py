import unittest

from fastapi import FastAPI, param_functions
from fastapi.testclient import TestClient

from knyhar.api.users import users_endpoint

endpoint_prefix = "/users/me"


class TestApiBooks(unittest.TestCase):
    def setUp(self):
        self.app = FastAPI()
        self.app.include_router(users_endpoint)
        self.test_client = TestClient(self.app)

    def test_get_user_info(self):
        response = self.test_client.get(endpoint_prefix)

        self.skipTest("Not implemented!")

    def test_get_favorite_books(self):
        response = self.test_client.get(endpoint_prefix + "/favorites")

        self.skipTest("Not implemented!")

    def test_add_favorite_books(self):
        response = self.test_client.post(
            endpoint_prefix + "/favorites", json={"book_id": 1})

        self.skipTest("Not implemented!")

    def test_delete_favorite_book(self):
        response = self.test_client.delete(endpoint_prefix + "/favorites")

        self.skipTest("Not implemented!")

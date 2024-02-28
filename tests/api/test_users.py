import unittest

from fastapi.testclient import TestClient

from knyhar.knyhar import create_app
from knyhar.api import users
from knyhar.settings import Settings

from tests.mocks.database.database import MockDatabase
from tests.api import ApiTests

endpoint_prefix = "/users/me"


class TestApiUsers(ApiTests):
    def test_get_user_info(self):
        response = self.test_client.get(endpoint_prefix)

        self.assertEqual(response.status_code, 200)

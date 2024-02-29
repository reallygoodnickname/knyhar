import unittest
from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from knyhar.models.users import User
from knyhar.settings import Settings

from jose import jwt

from tests.mocks.database.database import MockDatabase
from knyhar.knyhar import routes, create_app, protected


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.test_user = User(username="test", password="test", admin="True")

        # Get application parts
        self.database = MockDatabase()
        self.settings = Settings()

        self.database.users.get_user_by_username = MagicMock(
            return_value=self.test_user)
        self.database.users.get = MagicMock(return_value=self.test_user)

        # Setup application
        self.settings.secret_key = "dev"
        self.app = create_app(routes, self.settings, self.database, protected)

        # Bearer tokens for different access levels
        self.bearer_token = jwt.encode({"id": 1, "iat": 0, "exp": 9999999999999},
                                       self.settings.secret_key, algorithm="HS256")

        # Create test application
        self.test_client = TestClient(self.app)
        self.test_client.headers["Authorization"] = "Bearer " + \
            self.bearer_token

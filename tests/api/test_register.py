import unittest
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from knyhar.knyhar import create_app
from knyhar.api import register
from knyhar.settings import Settings
from tests.api import ApiTests

from tests.mocks.database.database import MockDatabase

prefix = register.endpoint.prefix

test_user = {
    "username": "test",
    "password": ""
}


class TestApiRegister(ApiTests):
    def test_register_incorrect_pass_len(self):
        """ Register user with too short or too long password """
        test_user["password"] = "A"*(self.app.extra["settings"].max_pass+1)
        result = self.test_client.post(prefix, json=test_user)
        self.assertEqual(result.status_code, 400)

        test_user["password"] = ""
        result = self.test_client.post(prefix, json=test_user)
        self.assertEqual(result.status_code, 400)

    def test_register_correct_data(self):
        """ Register user with correct data """
        self.database.users.add = MagicMock(return_value=True)

        test_user["password"] = "A"*(self.app.extra["settings"].max_pass)
        result = self.test_client.post(prefix, json=test_user)

        self.assertTrue(result.status_code, 200)

    def test_register_username_taken(self):
        """ Try to register with existing username """
        test_user["password"] = "A"*(self.app.extra["settings"].max_pass)

        self.database.users.add = MagicMock(return_value=False)
        result = self.test_client.post(prefix, json=test_user)

        self.assertEqual(result.status_code, 400)

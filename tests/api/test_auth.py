# Test auth API endpoints
import unittest
from unittest.mock import MagicMock
from argon2 import PasswordHasher

from fastapi import FastAPI
from fastapi.testclient import TestClient

from knyhar.api import auth
from knyhar.knyhar import create_app
from knyhar.models.users import User
from knyhar.settings import Settings
from tests.api import ApiTests
from tests.mocks.database.database import MockDatabase

endpoint_prefix = "/auth"

test_user_obj = User(id=1, username="username",
                     password=PasswordHasher().hash("password"),
                     admin=False)

test_user = {
    "username": "username",
    "password": "password",
}


class TestApiAuth(ApiTests):
    def test_auth_user_exists(self):
        """ Test authentication for existing user """
        self.database.users.get_user_by_username = MagicMock(
            return_value=test_user_obj)

        response = self.test_client.post("/auth", data=test_user)
        self.assertEqual(response.status_code, 200)

    def test_auth_user_doesnt_exist(self):
        """ Test authentication for wrong username """
        self.database.users.get_user_by_username = MagicMock(
            return_value=None)

        response = self.test_client.post("/auth", data=test_user)
        self.assertEqual(response.status_code, 401)

    def test_auth_user_incorrect_password(self):
        """ Test authentication for wrong password """
        user = {
            "username": "username",
            "password": "passwordd",
        }

        self.database.users.get_user_by_username = MagicMock(
            return_value=test_user_obj)

        response = self.test_client.post("/auth", data=user)
        self.assertEqual(response.status_code, 401)

    def test_auth_wrong_password_len(self):
        """ Test authentication for wrong password length """
        user = {
            "username": "username",
            "password": "A"*self.app.extra["settings"].max_pass,
        }

        self.database.users.get_user_by_username = MagicMock(
            return_value=test_user_obj)

        response = self.test_client.post("/auth", data=user)
        self.assertEqual(response.status_code, 401)

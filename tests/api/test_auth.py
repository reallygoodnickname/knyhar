# Test auth API endpoints

import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from library.api.auth import auth_endpoint

endpoint_prefix = "/auth"


class TestApiAuth(unittest.TestCase):
    def setUp(self):
        self.app = FastAPI()
        self.app.include_router(auth_endpoint)
        self.test_client = TestClient(self.app)

    def test_auth_user(self):
        test_user = {
            "username": "test",
            "password": "test"
        }

        response = self.test_client.post("/auth/", json=test_user)

        self.skipTest("Not implemented!")

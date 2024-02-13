import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from knyhar.api.export import export_endpoint

endpoint_prefix = "/export"


class TestApiAuth(unittest.TestCase):
    def setUp(self):
        self.app = FastAPI()
        self.app.include_router(export_endpoint)
        self.test_client = TestClient(self.app)

    def test_export_books(self):
        response = self.test_client.get(endpoint_prefix+"/")

        self.skipTest("Not implemented!")

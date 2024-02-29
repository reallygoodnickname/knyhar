import unittest
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from knyhar.api import export

from knyhar.models.books import Book
from knyhar.models.tags import Tag

from knyhar.knyhar import create_app
from knyhar.settings import Settings
from tests.api import ApiTests

from tests.mocks.database import database

endpoint_prefix = "/export"

mock_books_db = [
    Book(id=1, name="Test1", description="test", author="Test",
         tags=[Tag(name="Sci-Fi")], price=1.00, ),
    Book(id=2, name="Test2", description="test", author="Test",
         tags=[Tag(name="Fiction")], price=2.00),
    Book(id=3, name="Test3", description="test", author="Test",
         tags=[Tag(name="Horror")], price=3.00)
]


# Expected result from input
expected_result = """id,name,description,author,tags,price
1,Test1,test,Test,['Sci-Fi'],1.0
2,Test2,test,Test,['Fiction'],2.0
3,Test3,test,Test,['Horror'],3.0
"""


class TestAPIExport(ApiTests):
    def test_export_books(self):
        self.database.books.get_all = MagicMock(return_value=mock_books_db)
        response = self.test_client.get(endpoint_prefix+"/")

        self.assertEqual(response.text.replace('\r', ""), expected_result)
        self.assertEqual(response.status_code, 200)

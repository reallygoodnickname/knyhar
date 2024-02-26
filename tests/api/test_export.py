import unittest
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from knyhar.api import export

from knyhar.models.books import Book
from knyhar.models.tags import Tag

from knyhar.knyhar import create_app
from knyhar.settings import Settings

from tests.mocks.database import database

endpoint_prefix = "/export"

mock_books_db = [
    Book(id=1, name="Test1", description="test", author="Test",
         tags=[Tag(id=2, name="Sci-Fi")], price=1.00, ),
    Book(id=2, name="Test2", description="test", author="Test",
         tags=[Tag(id=3, name="Fiction")], price=2.00),
    Book(id=3, name="Test3", description="test", author="Test",
         tags=[Tag(id=1, name="Horror")], price=3.00)
]


# Expected result from input
expected_result = """id,name,description,author,price,tags,fans
1,Test1,test,Test,1.0,['Sci-Fi'],[]
2,Test2,test,Test,2.0,['Fiction'],[]
3,Test3,test,Test,3.0,['Horror'],[]
"""


class TestApiExport(unittest.TestCase):
    def setUp(self):
        self.database = database.MockDatabase()
        self.app = create_app([export.endpoint], Settings(), self.database)

        self.test_client = TestClient(self.app)

    def test_export_books(self):
        self.database.books.get_all = MagicMock(return_value=mock_books_db)
        response = self.test_client.get(endpoint_prefix+"/")

        self.assertEqual(response.text.replace('\r', ""), expected_result)
        self.assertEqual(response.status_code, 200)

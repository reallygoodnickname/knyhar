import logging

from sqlalchemy import create_engine, select
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy.orm import Session

from knyhar.models import Base
from knyhar.models.books import Book
from knyhar.models.users import User

from knyhar.database.users import UsersDatabase
from knyhar.database.books import BooksDatabase
from knyhar.database.tags import TagsDatabase


class Database():
    default_dbms_name = "postgresql"
    default_dbapi = "psycopg"
    default_db_name = "knyhar"

    def __init__(self, host: str, username: str, password: str,
                 db_name: str = default_db_name,
                 dbms_name: str = default_dbms_name, dbapi: str = default_dbapi):

        # Database credentials
        self.host = host
        self.username = username
        self.password = password
        self.db_name = db_name

        # Connector details
        self.dbms_name = dbms_name
        self.dbapi = dbapi

        self._connect_to_database()

        # DatabaseSubclasses
        self.users = UsersDatabase(self)
        self.books = BooksDatabase(self)
        self.tags = TagsDatabase(self)

    def _connect_to_database(self):
        scheme = self.dbms_name + "+" + self.dbapi
        credentials = f"{self.username}:{self.password}"

        URI = f"{scheme}://{credentials}@{self.host}/{self.db_name}"

        self.engine = create_engine(URI)
        Base.metadata.create_all(self.engine)

# Subclass used for functions related to books
from typing import List, Sequence, Tuple
from sqlalchemy import select

import sqlalchemy.exc
from sqlalchemy.orm import Session

from knyhar.models.books import Book
from knyhar.database import SubclassTemplate


class BooksDatabase(SubclassTemplate):
    def __init__(self, database_obj):
        super().__init__(database_obj, Book)

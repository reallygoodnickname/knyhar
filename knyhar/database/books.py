# Subclass used for functions related to books
from typing import List, Sequence, Tuple
from sqlalchemy import select

import sqlalchemy.exc
from sqlalchemy.orm import Session

from knyhar.models.books import Book


class BooksDatabase():
    def __init__(self, parent_obj):
        self.parent_obj = parent_obj
        self.engine = parent_obj.engine

    def get(self, id: int) -> Book | None:
        """
        Get book by ID

        Arguments:
            id: Book id
        Returns:
            Book | None: This function will return Book 
            object or None if book doesn't exist
        """
        with Session(self.engine) as session:
            book = session.get(Book, id)

            return book

    def get_all(self):
        """
        Get all books

        Arguments:
            None: This function doesn't take any arguments
        Returns:
            books: List of all books from database
        """
        with Session(self.engine) as session:
            books = session.execute(select(Book)).all()

            return books

    def add(self, book: Book) -> bool:
        """
        Add new book

        Arguments:
            book: Book to add
        Returns:
            bool: True - added successfully
                  False - book already exists
        """
        with Session(self.engine) as session:
            try:
                session.add(book)
                session.commit()
            except sqlalchemy.exc.IntegrityError:
                return False

            return True

    def remove(self, id: int):
        """ 
        Remove book 

        Arguments:
            id: Book ID to remove
        Returns:
            bool: True - removed successfully
                  False - book doesn't exist
        """
        with Session(self.engine) as session:
            book = self.get(id)

            if book is None:
                return False

            session.delete(book)
            session.commit()

            return True

    def add_tags(self, id: int, tags: List[str]) -> bool:
        """
        Add tags to a book

        Arguments:
            id: This function doesn't take any arguments
            tags: List of tags to add
        Returns:
            Bool: True - added successfully
                  False - failed to add tag 
        """
        return True

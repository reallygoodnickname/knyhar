from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Association tables

users_books_assoc_table = Table(
    "users_books_association_table",
    Base.metadata,
    Column("left_id", ForeignKey("users.id"), primary_key=True),
    Column("right_id", ForeignKey("books.id"), primary_key=True),
)

books_tags_assoc_table = Table(
    "books_tags_association_table",
    Base.metadata,
    Column("left_id", ForeignKey("books.id")),
    Column("right_id", ForeignKey("tags.id")),
)

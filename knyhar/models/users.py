from __future__ import annotations

from typing import List

from sqlalchemy import Boolean, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from knyhar.models import Base, users_books_assoc_table
import knyhar.models.books

from pydantic import BaseModel


class UserModel(BaseModel):
    id: int | None = None
    username: str
    admin: bool
    favorites: list[knyhar.models.books.BookModel]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False,
                                          unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False,
                                          unique=False)
    admin: Mapped[bool] = mapped_column(Boolean, nullable=False,
                                        default=False)
    favorites: Mapped[List[knyhar.models.books.Book]] = relationship(
        secondary=users_books_assoc_table, back_populates="fans"
    )

    def get_pydantic_model(self, session) -> UserModel:
        """ Convert current user into a pydantic model

        Arguments:
            None: this function doesn't 
        Returns:
            UserModel: Returns created user model
        """

        session.add(self)
        favorites = [book.get_pydantic_model(
            session) for book in self.favorites]

        return UserModel(id=self.id, username=self.username, admin=self.admin,
                         favorites=favorites)

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, password={self.password}, admin={self.admin}, favorties={self.favorites})'

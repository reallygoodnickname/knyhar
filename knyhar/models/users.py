from __future__ import annotations

from typing import List

from sqlalchemy import Boolean, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from knyhar.models import Base, users_books_assoc_table
import knyhar.models.books


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False,
                                          unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False,
                                          unique=False)
    admin: Mapped[bool] = mapped_column(Boolean, nullable=False,
                                        default=False)
    favorites: Mapped[List[knyhar.models.books.Book]] = relationship(
        secondary=users_books_assoc_table, back_populates="fans"
    )

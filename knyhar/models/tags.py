from __future__ import annotations

from pydantic import BaseModel

from knyhar.models import Base, books_tags_assoc_table
from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

import knyhar.models.books


class TagModel(BaseModel):
    name: str


class Tag(Base):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(
        String(32), primary_key=True, nullable=False, unique=True)

    books: Mapped[List[knyhar.models.books.Book]] = relationship(
        secondary=books_tags_assoc_table, back_populates="tags"
    )

    def get_pydantic_model(self) -> TagModel:
        return TagModel(name=self.name)

    def __repr__(self):
        return f'Tag(name={self.name}, books={self.books})'

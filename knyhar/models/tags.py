from __future__ import annotations

from knyhar.models import Base, books_tags_assoc_table
from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

import knyhar.models.books


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    books: Mapped[List[knyhar.models.books.Book]] = relationship(
        secondary=books_tags_assoc_table, back_populates="tags"
    )

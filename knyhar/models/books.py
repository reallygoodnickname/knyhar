from __future__ import annotations

from typing import List
from sqlalchemy import (Float,
                        String,
                        Integer,
                        ARRAY)
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)

from knyhar.models import (Base,
                           users_books_assoc_table,
                           books_tags_assoc_table)
from knyhar.models.tags import Tag
import knyhar.models.users


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=False,
                                      nullable=False)
    description: Mapped[str] = mapped_column(String(1024), unique=False,
                                             nullable=False)
    author: Mapped[str] = mapped_column(String(256),
                                        unique=False, nullable=False)
    tags: Mapped[List["Tag"]] = relationship(
        secondary=books_tags_assoc_table, back_populates="books"
    )
    fans: Mapped[List[knyhar.models.users.User]] = relationship(
        secondary=users_books_assoc_table, back_populates="favorites"
    )
    price: Mapped[float] = mapped_column(Float, unique=False,
                                         nullable=False)

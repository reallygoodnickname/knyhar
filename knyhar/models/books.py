from __future__ import annotations

from typing import List
from pydantic import BaseModel
from sqlalchemy import (Float,
                        String,
                        Integer)
from sqlalchemy.orm import (Mapped, Session,
                            mapped_column,
                            relationship)

from knyhar.models import (Base,
                           users_books_assoc_table,
                           books_tags_assoc_table)
from knyhar.models.tags import Tag, TagModel
import knyhar.models.users


class BookModel(BaseModel):
    id: int | None = None
    name: str
    description: str
    author: str
    tags: list[TagModel]
    price: float


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

    def get_pydantic_model(self, session: Session) -> BookModel:
        """
        Convert current book into a pydantic book model

        Arguments:
            None: this function doesn't take any arguments
        Returns:
            BookModel: Returns created book model suitable for
                       returning from endpoints
        """
        session.add(self)
        return BookModel(id=self.id, name=self.name, description=self.description,
                         author=self.author, tags=[
                             tag.get_pydantic_model() for tag in self.tags],
                         price=self.price)

    def __repr__(self):
        return f'Book(id={self.id}, name={self.name}, description={self.description},' + \
            f'author={self.author}, tags={self.tags}, fans={self.fans}, price={self.price})'

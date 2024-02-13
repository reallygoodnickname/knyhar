# Books endpoint

from fastapi import APIRouter
from pydantic import BaseModel

books_endpoint = APIRouter(prefix="/books",
                           tags=["books"])


class Book(BaseModel):
    name: str
    description: str
    author: list[str]
    genre: list[str]
    price: float


# Get all books or info about specific book
@books_endpoint.get("/")
def get_books(id: int | None = None):
    return {"msg: not implemented!"}, 501


# Add new book (admin only)
@books_endpoint.post("/")
def add_book(book: Book):
    return {"msg: not implemented!"}, 501


# Delete book by id (admin only)
@books_endpoint.post("/")
def delete_book(id: int):
    return {"msg: not implemented"}, 501

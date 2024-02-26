# Books endpoint
from knyhar.models.books import (Book,
                                 BookModel)

from fastapi import (APIRouter,
                     Response,
                     Request)

from pydantic import BaseModel

endpoint = APIRouter(prefix="/books", tags=["books"])


@endpoint.get("/")
def get_all_books(request: Request, response: Response):
    # Return all books in JSON format
    books = request.app.extra["database"].books

    response.status_code = 200

    _books = books.get_all()
    res = []

    for book in _books:
        res.append(book.get_pydantic_model())

    return res


@endpoint.get("/{id}")
def get_book(request: Request, response: Response, id: int):
    # Get info about one specific book
    books = request.app.extra["database"].books

    book = books.get(id)
    if book is None:
        response.status_code = 400
        return {"code": 400,
                "msg": "Book with such ID doesn't exist!"}

    return book.get_pydantic_model()


@endpoint.post("/")
def add_book(request: Request, book: BookModel, response: Response):
    books = request.app.extra["database"].books

    _book = Book(name=book.name, description=book.description,
                 author=book.author, price=book.price)

    if not books.add(_book):
        response.status_code = 400
        return {"code": 400,
                "msg": "Book already exists!"}
    else:
        response.status_code = 200
        return {"code": 200,
                "msg": "Added successfully!"}


@endpoint.delete("/{id}")
def delete_book(request: Request, id: int, response: Response):
    books = request.app.extra["database"].books

    if not books.remove(id):
        response.status_code = 400
        return {"code": 400,
                "msg": "Book doesn't exist!"}
    else:
        response.status_code = 200
        return {"code": 200,
                "msg": "Book removed successfully!"}

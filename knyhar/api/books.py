# Books endpoint
from typing import Annotated


from sqlalchemy.orm import Session

from knyhar.models.users import User
from knyhar.models.books import (Book,
                                 BookModel)

from knyhar.api.auth import get_user_from_token

from fastapi.responses import JSONResponse
from fastapi import (APIRouter,
                     HTTPException,
                     Response,
                     Depends,
                     Request)

endpoint = APIRouter(prefix="/books", tags=["books"])


@endpoint.get("/")
def get_all_books(request: Request, response: Response) -> list[BookModel]:
    # Return all books in JSON format
    books = request.app.extra["database"].books

    response.status_code = 200

    _books = books.get_all()
    res = []

    for book in _books:
        with Session(books.engine) as session:
            res.append(book.get_pydantic_model(session))

    return res


@endpoint.get("/{id}")
def get_book(request: Request, id: int) -> BookModel:
    # Get info about one specific book
    books = request.app.extra["database"].books

    book = books.get(id)
    if book is None:
        raise HTTPException(status_code=400,
                            detail="Book with such ID doesn't exist!")

    with Session(books.engine) as session:
        return book.get_pydantic_model(session)


@endpoint.post("/")
def add_book(request: Request, book: BookModel, user: Annotated[User, Depends(get_user_from_token)]) -> JSONResponse:
    books = request.app.extra["database"].books
    tags = request.app.extra["database"].tags

    _book = Book(name=book.name, description=book.description,
                 author=book.author, tags=[], price=book.price)

    for tag in book.tags:
        res = tags.get(tag)
        if res is None:
            raise HTTPException(status_code=400,
                                detail=f'Tag "{tag}" is not found!')

        _book.tags.append(res)

    if not books.add(_book):
        raise HTTPException(status_code=400,
                            detail="Book already exists!")
    else:
        return JSONResponse(status_code=200,
                            content={
                                "code": 200,
                                "msg": "Added successfully!"
                            })


@endpoint.delete("/{id}")
def delete_book(request: Request, id: int, user: Annotated[User, Depends(get_user_from_token)]) -> JSONResponse:
    books = request.app.extra["database"].books

    if not books.remove(id):
        raise HTTPException(status_code=400,
                            detail="Book doesn't exist!")
    else:
        return JSONResponse(status_code=200,
                            content={"code": 200,
                                     "msg": "Book removed successfully!"})

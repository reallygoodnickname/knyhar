# Users endpoint

from fastapi import (APIRouter,
                     Request,
                     Response)

endpoint = APIRouter(prefix="/users", tags=["users"])


# Return user information
@endpoint.get("/me")
def get_user_info():
    return {"msg: not implemented!"}, 501


# Return favorite books
@endpoint.get("/me/favorites")
def get_favorite_books():
    return {"msg: not implemented!"}, 501


# Add new book to user favorites
@endpoint.post("/me/favorites")
def add_favorite_book(request: Request, Response: Response, book_id: int):
    return {"msg: not implemented!"}, 501


# Delete book from the favorites
@endpoint.delete("/me/favorites")
def delete_favorite_book(book_id: int):
    return {"msg: not implemented!"}, 501

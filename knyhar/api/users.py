# Users endpoint

from typing import Annotated
from fastapi import (APIRouter, Depends, HTTPException,
                     Request)
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from knyhar.models.users import UserModel, User
from knyhar.models.books import BookModel
from knyhar.api.auth import get_user_from_token

from knyhar.database.exc import (EntityNotFound,
                                 EntityAlreadyAdded,
                                 EntityMissing)

endpoint = APIRouter(prefix="/users", tags=["users"])


# Return user information
@endpoint.get("/me")
def get_user_info(request: Request, user: Annotated[User, Depends(get_user_from_token)]) -> UserModel:
    database = request.app.extra["database"]

    with Session(database.engine) as session:
        session.add(user)
        return user.get_pydantic_model(session)


# Return favorite books
@endpoint.get("/me/favorites")
def get_favorite_books(request: Request, user: Annotated[User, Depends(get_user_from_token)]) -> list[BookModel]:
    database = request.app.extra["database"]

    with Session(database.engine) as session:
        session.add(user)
        favorites = user.get_pydantic_model(session).favorites

        return favorites


# Add new book to user favorites
@endpoint.put("/me/favorites/{id}")
def add_favorite_book(id: int, request: Request, user: Annotated[User, Depends(get_user_from_token)]) -> JSONResponse:
    database = request.app.extra["database"]

    try:
        database.users.add_favorite(user.id, id)
    except EntityNotFound as exc:
        raise HTTPException(status_code=404,
                            detail=f"Book with ID '{exc.entity}' doesn't exist!")
    except EntityAlreadyAdded:
        raise HTTPException(status_code=400,
                            detail="Book already added!")

    return JSONResponse(status_code=200,
                        content={
                            "code": 200,
                            "msg": "Added successfully!"
                        })


# Delete book from the favorites
@endpoint.delete("/me/favorites/{id}")
def delete_favorite_book(request: Request, id: int,
                         user: Annotated[User, Depends(get_user_from_token)]) -> JSONResponse:
    try:
        request.app.extra["database"].users.remove_favorite(user.id, id)
    except EntityMissing:
        raise HTTPException(status_code=400,
                            detail="Book not in favorites!")

    except EntityNotFound as exc:
        raise HTTPException(status_code=404,
                            detail=f"Book with ID '{exc.entity}' doesn't exist!")

    return JSONResponse(status_code=200,
                        content={
                            "code": 200,
                            "msg": "Removed successfully!"
                        })

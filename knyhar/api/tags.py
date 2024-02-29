# Tags endpoint

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import JSON
from sqlalchemy.orm import Session
from knyhar.models.books import BookModel

from knyhar.models.tags import Tag, TagModel

endpoint = APIRouter(prefix="/tags", tags=["tags"])


# Add new tag
@endpoint.post("/")
def add_tag(request: Request, tag: TagModel) -> JSONResponse:
    tags = request.app.extra["database"].tags
    res = tags.add(Tag(name=tag.name))

    if not res:
        raise HTTPException(status_code=400,
                            detail="Failed to add tag")

    return JSONResponse(status_code=200,
                        content={
                            "code": 200,
                            "msg": "Tag added successfully"
                        })


# Delete tag
@endpoint.delete("/{name}")
def remove_tag(request: Request, name: str) -> JSONResponse:
    tags = request.app.extra["database"].tags
    res = tags.remove(name)

    if not res:
        raise HTTPException(status_code=400, detail="Failed to remove tag")

    return JSONResponse(status_code=200,
                        content={
                            "code": 200,
                            "msg": "Tag removed successfully"
                        })


# Get all books with the same tag
@endpoint.get("/{name}")
def get_books_with_tag(request: Request, name: str) -> list[BookModel]:
    tags = request.app.extra["database"].tags
    tag = tags.get(name)

    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found!")

    with Session(tags.engine) as session:
        session.add(tag)
        return [book.get_pydantic_model(session) for book in tag.books]


# Get all tags
@endpoint.get("/")
def get_tags(request: Request) -> list[TagModel]:
    tags = request.app.extra["database"].tags

    return [tag.get_pydantic_model() for tag in tags.get_all()]

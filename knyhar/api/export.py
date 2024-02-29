# Export endpoint
from io import StringIO
from csv import writer

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from knyhar.models.books import BookModel

endpoint = APIRouter(prefix="/export", tags=["export"])


@endpoint.get("/")
def export_books(request: Request):
    # Get all books from database
    database = request.app.extra["database"]
    books = database.books.get_all()

    out = StringIO()
    csv_writer = writer(out)

    # Convert object to csv
    with Session(database.engine) as session:
        dict_books = [book.get_pydantic_model(
            session).model_dump() for book in books]

        csv_writer.writerow(BookModel.__annotations__)
        for book in dict_books:
            csv_writer.writerow(book.values())

    # Make response
    response = StreamingResponse(iter([out.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=books.csv"
    response.status_code = 200

    return response

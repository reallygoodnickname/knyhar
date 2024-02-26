# Export endpoint
from io import StringIO
from csv import writer

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from knyhar.models.books import Book

endpoint = APIRouter(prefix="/export", tags=["export"])


# Exports all books in CSV format (admin only)
@endpoint.get("/")
def export_books(request: Request):
    # Get all books from database
    db = request.app.extra["database"]
    books = db.books.get_all()

    out = StringIO()
    csv_writer = writer(out)

    # Get all keys from that books table
    mapper = Book.__mapper__
    columns = mapper.columns.keys()
    relationships = mapper.relationships.keys()

    csv_writer.writerow(columns+relationships)

    # Convert object to csv
    for book in books:
        row = [getattr(book, column) for column in columns]

        # Append tags (as names) and fans (as IDs)
        row.append([tag.name for tag in book.tags])
        row.append([fan.id for fan in book.fans])

        csv_writer.writerow(row)

    # Make response
    response = StreamingResponse(iter([out.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=books.csv"
    response.status_code = 200

    return response

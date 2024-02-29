import uvicorn

from fastapi import APIRouter, FastAPI

from knyhar.database.database import Database
from knyhar.settings import Settings
from knyhar.api import (auth,
                        register,
                        export,
                        books,
                        users,
                        tags)


# Application routes
routes = [
    auth.endpoint,          # Authentication endpoint
    register.endpoint,      # Register endpoint
    books.endpoint,         # Books endpoint
    export.endpoint,        # Export endpoint
    users.endpoint,         # Users endpoint
    tags.endpoint           # Tags endpoint
]

# Pages that should be available to admin only
protected = [
    "export_books",         # Export books in CSV
    "delete_book",          # Delete book
    "add_book",             # Add new book
    "add_tag",              # Add new tag
    "remove_tag",           # Remove tag
]


def create_app(routes: list[APIRouter], settings: Settings,
               database: Database, protected: list[str]) -> FastAPI:
    """
    Application factory

    Arguments:
        database: Database object
    Returns:
        app: FastAPI application
    """
    app = FastAPI()

    app.extra["database"] = database
    app.extra["settings"] = settings
    app.extra["protected"] = protected

    for route in routes:
        app.include_router(route)

    return app


def main():
    settings = Settings()

    database = Database(host=settings.host,
                        username=settings.db_username,
                        password=settings.db_password)

    app = create_app(routes, settings, database, protected)

    uvicorn.run(app, port=8080, log_level="warning")


if __name__ == "__main__":
    main()

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


def create_app(routes: list[APIRouter], settings: Settings,
               database: Database) -> FastAPI:
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

    for route in routes:
        app.include_router(route)

    return app


def main():
    settings = Settings()

    database = Database(host=settings.host,
                        username=settings.db_username,
                        password=settings.db_password)

    app = create_app(routes, settings, database)

    uvicorn.run(app, port=8080, log_level="warning")


if __name__ == "__main__":
    main()

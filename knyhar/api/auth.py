# Authentication endpoint
from fastapi import APIRouter, Request, Response

from pydantic import BaseModel

from knyhar.models.users import User

endpoint = APIRouter(prefix="/auth", tags=["auth"])


class auth_creds(BaseModel):
    username: str
    password: str


@endpoint.post("/")
def auth_user(request: Request, auth_creds: auth_creds,
              response: Response):

    users = request.app.extra["database"].users
    settings = request.app.extra["settings"]

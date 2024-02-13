# Authentication endpoint
from fastapi import APIRouter
from pydantic import BaseModel

auth_endpoint = APIRouter(prefix="/auth", tags=["auth"])


class auth_credentials(BaseModel):
    username: str
    password: str

# Perform user authentication, return secret key on success


@auth_endpoint.post("/")
def auth_user(auth_credentials: auth_credentials):
    return {"msg": "not implemented!"}, 501

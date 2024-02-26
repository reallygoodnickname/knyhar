# Authentication endpoint
from fastapi import (APIRouter,
                     Request,
                     Response)
from pydantic import BaseModel

from knyhar.models.users import User
from argon2 import PasswordHasher

endpoint = APIRouter(prefix="/register", tags=["register"])


class register_creds(BaseModel):
    username: str
    password: str


@endpoint.post("/")
def register_user(request: Request, register_creds: register_creds,
                  response: Response):
    users = request.app.extra["database"].users
    settings = request.app.extra["settings"]
    pass_len = len(register_creds.password)

    if pass_len > settings.max_pass or pass_len < settings.min_pass:
        response.status_code = 400
        return {
            "code": response.status_code,
            "msg": f"Incorrect password length! (max: {settings.max_pass}, " +
            f"min: {settings.min_pass})"
        }
    else:
        hashed_password = PasswordHasher().hash(register_creds.password)

        res = users.add(User(username=register_creds.username,
                             password=hashed_password, admin=False))
        if not res:
            response.status_code = 400
            return {
                "code": response.status_code,
                "msg": "Username already taken!"
            }
        else:
            response.status_code = 200
            return {
                "code": response.status_code,
                "msg": "Registered successfully!"
            }

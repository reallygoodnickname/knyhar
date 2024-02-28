# Authentication endpoint
import time
from jose import JWTError, jwt
from typing import Annotated

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from fastapi import (APIRouter,
                     Depends, HTTPException,
                     Request,
                     Response)
from fastapi.responses import JSONResponse
from fastapi.security import (OAuth2PasswordBearer,
                              OAuth2PasswordRequestForm)

from knyhar.models.users import User

endpoint = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


def get_user_from_token(request: Request, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    settings = request.app.extra["settings"]
    users = request.app.extra["database"].users

    try:
        # Decode token
        decoded_token = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm])

        user = users.get(decoded_token["id"])

        # Validate token
        if (user is not None and
                decoded_token["exp"] > time.time()):
            return user

        raise HTTPException(status_code=401, detail="Invalid token!")

    except JWTError:
        raise HTTPException(
            status_code=401, detail="Failed to validate bearer token!")


@ endpoint.post("/")
def auth_user(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
              response: Response):
    users = request.app.extra["database"].users
    settings = request.app.extra["settings"]

    incorrect_creds_error = JSONResponse(
        status_code=401,
        content={
            "code": 401,
            "msg": "Incorrect username or password!"
        }
    )

    # Check password length
    if not (settings.min_pass <= len(form_data.password) <= settings.max_pass):
        return incorrect_creds_error

    user = users.get_user_by_username(form_data.username)

    # Check if we've got user from database
    if user is None:
        return incorrect_creds_error

    # Verify password hash
    try:
        PasswordHasher().verify(hash=user.password,
                                password=form_data.password)
    except VerifyMismatchError:
        return incorrect_creds_error

    # Create token
    cur_time = time.time()

    token_data = {
        "id": user.id,
        "iat": cur_time,
        "exp": cur_time + settings.expire
    }

    token = jwt.encode(token_data, key=settings.secret_key,
                       algorithm=settings.algorithm)

    # Return authentication token
    return {
        "access_token": token,
        "token_type": "bearer"
    }

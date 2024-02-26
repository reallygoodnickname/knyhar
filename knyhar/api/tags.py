# Tags endpoint

from fastapi import APIRouter

endpoint = APIRouter(prefix="/tags", tags=["tags"])


# Add new tag
@endpoint.post("/")
def add_tag():
    return {"msg": "not implemented!"}, 501

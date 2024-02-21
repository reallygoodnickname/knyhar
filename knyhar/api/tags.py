# Tags endpoint

from fastapi import APIRouter

tags_endpoint = APIRouter(prefix="/tags", tags=["tags"])


# Add new tag
@tags_endpoint.post("/")
def add_tag():
    return {"msg": "not implemented!"}, 501

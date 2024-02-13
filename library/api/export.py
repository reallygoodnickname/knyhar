# Export endpoint

from fastapi import APIRouter

export_endpoint = APIRouter(prefix="/export", tags=["export"])


# Exports all books in CSV format (admin only)
@export_endpoint.get("/")
def export_books():
    return {"msg": "not implemented!"}, 501

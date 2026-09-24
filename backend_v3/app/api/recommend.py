from fastapi import APIRouter
from app.models.request_model import (UserRequest, GroupDirectionRequest)
from app.services.recommender import recommend_places


router = APIRouter()

@router.post("/recommend")
def recommend(data: UserRequest):
    return recommend_places(data)


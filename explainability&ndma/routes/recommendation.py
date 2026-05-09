# routes/recommendation.py

from fastapi import APIRouter
from formatter.response_builder import build_response

router = APIRouter()

@router.post("/generate-recommendation")

def recommendation(data: dict):

    return build_response(data)
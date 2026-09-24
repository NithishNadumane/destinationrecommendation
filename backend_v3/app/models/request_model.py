from pydantic import BaseModel
from typing import List, Dict, Any


class Preference(BaseModel):
    type: str
    preference: int


class UserRequest(BaseModel):
    location: str
    max_distance: int
    trip_type: List[Preference]


class GroupDirectionRequest(BaseModel):
    location: str
    results: List[Dict[str, Any]]
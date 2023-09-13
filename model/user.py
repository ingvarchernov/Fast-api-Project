from pydantic import BaseModel
from typing import List

class UserResponse(BaseModel):
    id: int
    name: str
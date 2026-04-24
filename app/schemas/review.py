from pydantic import BaseModel, Field
from typing import Annoted

class Review(BaseModel):
    review: Annoted[int, Field(ge=1, le=5, examples=[5], description=[5])

from pydantic import BaseModel, Field
from typing import Annotated

class Review(BaseModel):
    review: Annotated[int, Field(ge=1, le=5, examples=[5], description="Voto da 1 a 5 ")]

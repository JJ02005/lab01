from pydantic import BaseModel, Field
from typing import Annotated

class BookPatch(BaseModel):
    title: str | None = None
    author: str | None = None



class Book(BaseModel):
    id: int
    title: str
    author: str
    review: Annotated[int, Field(ge=1, le=5)]


    model_config={
        "json_schema_extra": {
            "example": {
                "title": "Nome della rosa",
                "author": "umby eco",
                "review": "5",

            }
        }
    }

books= {
        0: Book (id=0, title="Il nome della rosa", author="umby eco", review=5),
        1: Book (id=1, title="Il gioco dei sei", author="umby eco", review=1),
        2: Book (id=2, title="Il gioco dei sei", author="umby eco", review=5),
        }
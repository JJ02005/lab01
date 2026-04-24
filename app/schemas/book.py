from pydantic import BaseModel, Field
from typing import Annoted

class Book(BaseModel):
    id: int
    title: str
    author: str
    review: Annoted[int, Field(ge=1, le=5)]


    model_config={
        "json_schema_extra": {
            "example": { [
                "title": "Nome della rosa",
                "author": "umby eco",
                "review": "5",

            }
        ]
        }
    }

    book= {
        
    }
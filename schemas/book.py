from pydantic import BaseModel, Field
from typing import Optional
from pydantic import ConfigDict

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    description: Optional[str] = None
    year: int = Field(..., ge=0)
    status: str = Field(default="available", min_length=1)


class BookResponse(BookCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
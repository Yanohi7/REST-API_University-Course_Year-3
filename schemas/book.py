from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    description: Optional[str] = None
    year: int = Field(..., ge=0)
    status: str = Field(default="available", min_length=1)


class BookResponse(BookCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PaginatedBookResponse(BaseModel):
    items: list[BookResponse]
    next_cursor: Optional[str] = None
    has_more: bool
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, min_length=1)
    year: int = Field(..., ge=0)
    status: str = Field(default="available", min_length=1) # available or issued

class BookResponse(BookCreate):
    id: UUID




from pydantic import BaseModel,ConfigDict, Field
from datetime import datetime, timezone
from enum import Enum

class Genre(str, Enum):
    FICTION="fiction"
    SCIFI="scifi"
    HORROR="horror"
    HISTORY="history"
    TECH="tech"

class BookCreate(BaseModel):
    title:str=Field(min_length=1,max_length=150)
    author:str=Field(min_length=1,max_length=50)
    genre:Genre
    available_copies:int=Field(default=1,ge=0)

class BookRead(BookCreate):
    id:int
    model_config=ConfigDict(from_attributes=True)

class BorrowCreate(BaseModel):
    borrower_name:str=Field(min_length=1,max_length=111)
    book_id:int

class BorrowRead(BorrowCreate):
    id: int
    borrowed_at: datetime
    returned: bool
    model_config = ConfigDict(from_attributes=True)

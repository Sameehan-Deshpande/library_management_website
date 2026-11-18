from sqlalchemy import ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped,mapped_column
from src.test.database import Base

class Book(Base):
    __tablename__= "books"

    id: Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]
    author:Mapped[str]
    genre:Mapped[str]
    available_copies:Mapped[int]=mapped_column(default=1)

class BorrowRecord(Base):
    __tablename__="borrow_records"

    id:Mapped[int]=mapped_column(primary_key=True)
    borrower_name:Mapped[str]
    book_id:Mapped[str]=mapped_column(ForeignKey("books.id"))
    borrowed_at:Mapped[datetime]=mapped_column(default=lambda:datetime.now(timezone.utc))
    returned:Mapped[bool]=mapped_column(default=False)

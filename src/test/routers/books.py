from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from src.test.database import SessionDep
from src.test.models import Book, BorrowRecord
from src.test.schema import BorrowCreate,BookCreate,BaseModel,BookRead,BorrowRead,Genre

router=APIRouter(prefix="/books",tags=["books"])

@router.post("/",response_model=BookRead)
def create_book(book_in:BookCreate,session:SessionDep):
    new_book=Book(
        title=book_in.title,
        author=book_in.author,
        genre=book_in.genre.value,
        available_copies=book_in.available_copies,
    )
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book

@router.get("/",response_model=list[BookRead])
def get_books(session:SessionDep,genre:Genre|None=None,available_only:bool=False):
    statement=select(Book)
    if genre:
        statement=statement.where(Book.genre == genre.value)
    if available_only:
        statement=statement.where(Book.available_copies > 0)
    return session.scalars(statement).all()

@router.delete("/{book_id}")
def delete_book(book_id:int,session:SessionDep,):
    book=session.get(Book,book_id)
    active_borrow=session.scalars(select(BorrowRecord).where(BorrowRecord.book_id == book_id, BorrowRecord.returned == False))
    if active_borrow:
        raise HTTPException(status_code=400,detail="can not delete borrowed book")
    session.delete(book)
    session.commit()
    return {"deleted_book_id":book_id}



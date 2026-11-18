from fastapi import HTTPException,APIRouter
from sqlalchemy import select

from src.test.models import BorrowRecord,Book
from src.test.database import SessionDep
from src.test.schema import BorrowCreate,BookRead,BorrowRead

router=APIRouter(prefix="/borrows", tags=["borrows"])

@router.post("/", response_model=BorrowRead)
def borrow_book(borrow_in:BorrowCreate,session:SessionDep):
    book=session.get(Book,borrow_in.book_id)
    if not book:
        raise HTTPException(status_code=400,detail="Book Not found")
    if book.available_copies <=0:
        raise HTTPException(status_code=404, detail="No available copies")
    book.available_copies-=1
    new_borrow=BorrowRecord(borrower_name=borrow_in.borrower_name,
        book_id=borrow_in.book_id,)
    session.add(new_borrow)
    session.commit()
    session.refresh(new_borrow)
    return new_borrow
@router.get("/{borrow_id}/return",response_model=BorrowRead)
def return_book(borrow_id:int,session:SessionDep):
    record=session.get(BorrowRecord,borrow_id)
    if not record:
        raise HTTPException(status_code=404, detail="record not found")
    if record.returned is True:
        raise HTTPException(status_code=400, detail="Book already returned")
    record.returned=True
    book=session.get(Book,record.book_id)
    if not book:
        raise HTTPException(status_code=404,detail="Book not found")
    book.available_copies+=1
    session.commit()
    session.refresh(book)
    return record
@router.get("/",response_model=list[BorrowRead])
def borrow_record(session:SessionDep,active_only: bool=False):
    statement=select(BorrowRecord)
    if active_only:
        statement=statement.where(BorrowRecord.returned==False)
    return session.scalars(statement).all()


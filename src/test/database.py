from sqlalchemy import create_engine, column
from fastapi import Depends
from sqlalchemy.orm import Session,DeclarativeBase
from typing import Annotated


Url="sqlite:///members.db"
engine=create_engine(Url,connect_args={"check_same_thread": False})

class Base(DeclarativeBase):
    pass

def get_db_and_tables():
    Base.metadata.create_all(bind=engine)
    
def get_session():
    with Session(engine) as session:
        yield session

SessionDep= Annotated[Session, Depends(get_session)]



from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from src.test.database import get_db_and_tables
from src.test.routers import books, borrows


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_db_and_tables()
    yield


app = FastAPI(title="Library Tracker API", lifespan=lifespan)

app.include_router(books.router)
app.include_router(borrows.router)

@app.get("/")
def get_frontend():
    return FileResponse(r"C:\Users\ADMIN\test\src\static\index.html")
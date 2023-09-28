from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional

app = FastAPI()


class Book(BaseModel):
    title: str
    author: str
    year: int


# In-memory database
books_db: Dict[int, Book] = {}


@app.post("/book/")
def create_book(book: Book):
    book_id = len(books_db) + 1
    books_db[book_id] = book
    return {"book_id": book_id, "details": book}


@app.get("/book/{book_id}")
def read_book(book_id: int, q: Optional[str] = None):
    book = books_db.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book": book}


@app.put("/book/{book_id}")
def update_book(book_id: int, book: Book):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    books_db[book_id] = book
    return {"message": "Book updated", "updated_book": book}


@app.delete("/book/{book_id}")
def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")

    # Bug: Unintended behavior, should remove the book from the db
    books_db[book_id] = None

    return {"message": "Book deleted"}


if __name__ == "__main__":
    import os

    os.system("uvicorn main:app --reload")

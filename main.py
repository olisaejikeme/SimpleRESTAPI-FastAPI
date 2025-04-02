from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory storage to store the books
fake_db = {}

# Create a book model
class Book(BaseModel):
    title: str
    author: str
    year_published: int | None = None

# Helper function to generate book ID
def generate_id():
    return str(len(fake_db) + 1)

@app.get("/")
async def root():
    return {"Hello": "World"}

# Get all books
@app.get("/books", response_model=List[Book])
async def get_books():
    return list(fake_db.values())

# Add a book
@app.post("/books", response_model=Book)
async def add_book(book: Book):
    book_id = generate_id()
    fake_db[book_id] = book
    return book

# Get book by ID
@app.get("/books/{book_id}", response_model=Book)
async def get_book_by_id(book_id: str):
    book = fake_db.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Update a book by ID
@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: str, book: Book):
    if book_id not in fake_db:
        raise HTTPException(status_code=404, detail="Book not found")
    fake_db[book_id] = book
    return book

# Delete a book
@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    if book_id not in fake_db:
        raise HTTPException(status_code=404, detail="Book not found")
    del fake_db[book_id]
    return f"Book with id: {book_id} has been deleted successfully"




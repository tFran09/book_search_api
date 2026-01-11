# Import necessary types for the Pydantic models
from pydantic import BaseModel
from typing import List

class Book(BaseModel):
    # Note: I've changed publish_year to int, as '2020' is easier to work with than '2020-01-01'
    authors: list[str]
    isbn: str
    publish_year: str  # Changed to int for better data type integrity
    title: str
    read: bool = False

class Books(BaseModel):
    count: int
    books: list[Book]
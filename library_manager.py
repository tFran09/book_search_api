from tinydb import TinyDB, Query
from typing import List
from book_models import Book

class LibraryManager:
    def __init__(self, db_path: str = "library.json"):
        # Initialize TinyDB with a local JSON file
        self.db = TinyDB(db_path)
        self.table = self.db.table('books')

    def add_book(self, book: Book) -> str:
        BookQuery = Query()
        # Check if the book already exists in the library by ISBN
        if self.table.search(BookQuery.isbn == book.isbn):
            return f"Book '{book.title}' is already in your library."
        
        # Save the Pydantic model as a dictionary
        self.table.insert(book.model_dump())
        return f"Book '{book.title}' has been added to your library!"

    def get_all_books(self) -> List[Book]:
        # Retrieve all records and convert them back into Book objects
        all_books_data = self.table.all()
        return [Book.model_validate(data) for data in all_books_data]

    def mark_book_as_read(self, isbn: str) -> bool:
        BookQuery = Query()
        # Update the 'read' field to True for the matching ISBN
        updated_ids = self.table.update({'read': True}, BookQuery.isbn == isbn)
        return len(updated_ids) > 0
from typing import Optional
from tabulate import tabulate
from book_api_client import BookAPIClient 
from book_models import Book, Books
from library_manager import LibraryManager

def print_book_details_vertical(book: Book):
    """
    Prints a single book's details vertically for maximum terminal width compatibility.
    """
    # NOTE: With Pydantic, you access attributes directly (book_data.title), 
    # not with .get() as you would for a dictionary.
    print(f"\n--- 📖 Book Details: {book.title} ---")
    
    # Prepare data as (Key, Value) pairs
    data = [
        # Access attributes directly
        ("ISBN", book.isbn),
        ("Title", book.title),
        # book_data.authors is already a list due to Pydantic
        ("Authors", ", ".join(book.authors)), 
        ("Published Year", book.publish_year),
        # You'll need to update your model or add a field if you want to display pages/publisher
        # For now, let's keep the existing fields:
        ("Status", "Read" if book.read else "To Read"),
    ]
    
    # Print as a two-column table with no borders
    print(tabulate(data, tablefmt="plain"))

def prompt_save_book(library: LibraryManager, book: Book):
    """Helper function to prompt user to save a book to their library."""
    print("\nWould you like to add this book?")
    print("1. Add to Library (Read)")
    print("2. Add to 'To Read' List")
    print("3. No")
    
    save_choice = input("Select an option: ")
    if save_choice == "1":
        book.read = True
        print(library.add_book(book))
    elif save_choice == "2":
        book.read = False
        print(library.add_book(book))

# --- MAIN EXECUTION LOGIC ---

def main():
    client = BookAPIClient()
    library = LibraryManager()

    while True:
        print("\n--- 📚 Book App Menu ---")
        print("1. Search by ISBN")
        print("2. Search by Title")
        print("3. Search by Author")
        print("4. View My Library")
        print("5. View 'To Read' List")
        print("6. Mark Book as Read")
        print("7. Exit")
        
        choice = input("\nSelect an option: ")

        if choice == "1":
            isbn = input("-- Please enter an ISBN --\n")
            book: Optional[Book] = client.get_book_by_isbn(isbn)
            if book:
                print_book_details_vertical(book)
                prompt_save_book(library, book)

        elif choice == "2":
            title = input("-- Please enter a book title --\n")
            search_results: Optional[Books] = client.search_books_by_title(title, exact=True)
            if search_results:
                print(f"\nTotal number of search results: {search_results.count}")
                for book in search_results.books:
                    print_book_details_vertical(book)
        
        elif choice == "3":
            author = input("-- Please enter an author name --\n")
            search_results: Optional[Books] = client.search_books_by_author(author, exact=True)
            if search_results:
                print(f"\nTotal number of search results: {search_results.count}")
                for book in search_results.books:
                    print_book_details_vertical(book)

        elif choice == "4":
            my_books = library.get_all_books()
            if not my_books:
                print("\nYour library is empty.")
            else:
                print(f"\n--- 🏠 My Library ({len(my_books)} books) ---")
                for book in my_books:
                    print_book_details_vertical(book)

        elif choice == "5":
            my_books = library.get_all_books()
            to_read_books = [book for book in my_books if not book.read]
            
            if not to_read_books:
                print("\nYou have no books in your 'To Read' list.")
            else:
                print(f"\n--- 📝 To Read List ({len(to_read_books)} books) ---")
                for book in to_read_books:
                    print_book_details_vertical(book)

        elif choice == "6":
            isbn = input("-- Please enter the ISBN of the book you have read --\n")
            if library.mark_book_as_read(isbn):
                print(f"Success! Book with ISBN {isbn} marked as read.")
            else:
                print("Could not find a book with that ISBN in your library.")

        elif choice == "7":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
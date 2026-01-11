import requests
from fastapi import FastAPI, HTTPException
from typing import Optional
from book_models import Book, Books

app = FastAPI(title="Book Lookup API")

@app.get("/search/{title}", response_model=Books)
def search_book(title: str, exact: bool = False):
    OPEN_LIBRARY_URL_BASE = "https://openlibrary.org/search.json"

    OPEN_LIBRARY_URL_SEARCH = OPEN_LIBRARY_URL_BASE + f"?title={title}&fields=title,author_name,first_publish_year,isbn"

    response = requests.get(OPEN_LIBRARY_URL_SEARCH)
    book_data = response.json()

    books = book_data.get("docs")

    book_set = []


    for book in books:
    # PROTECTION: Skip empty dictionaries {}
        if not book:
            continue

        # 1. Handle Titles and Authors safely
        book_title = book.get("title", "Untitled")
        
        if exact and book_title.lower() != title.lower():
            continue
            
        authors = book.get('author_name', ["Unknown Author"])

        # 2. Get the ISBN safely (Preferring ISBN-13 if possible)
        isbn_list = book.get("isbn", [])
        isbn_value = str(isbn_list[0]) if isbn_list else "Unknown ISBN"

        # 3. Handle Publish Year (The "Fallback" Logic)
        # Open Library has 'first_publish_year' (int) and 'publish_year' (list of ints)
        year_raw = book.get("first_publish_year")
        
        if year_raw:
            publish_year_value = str(year_raw)
        else:
            # Fallback to the first item in the publish_year list if first_publish_year is missing
            years_list = book.get("publish_year", [])
            publish_year_value = str(years_list[0]) if years_list else "N/A"

        # 4. Create the Book Object
        new_book = Book(
            authors = authors,
            isbn = isbn_value,
            publish_year = publish_year_value,
            title = book_title      
        )
        book_set.append(new_book)


    ret_books = Books(
        count = book_data.get("num_found"),
        books = book_set
    )

    return ret_books

@app.get("/search/author/{author_name}", response_model=Books)
def search_books_by_author(author_name: str, exact: bool = False) -> Optional[Books]:
    # 1. Construct URL for Open Library Author Search
    # Using the author parameter specifically filters the results
    OPEN_LIBRARY_URL_BASE = "https://openlibrary.org/search.json"

    search_url = OPEN_LIBRARY_URL_BASE + f"?author={author_name}&fields=title,author_name,first_publish_year,isbn"
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        book_data = response.json()
        
        book_set = []
        books = book_data.get("docs", [])

        for book in books:
            if not book:
                continue

            # Safe extraction logic (similar to your title search)
            authors = book.get('author_name', [author_name]) # Fallback to searched name
            
            if exact:
                if not any(a.lower() == author_name.lower() for a in authors):
                    continue

            isbn_list = book.get("isbn", [])
            isbn_value = str(isbn_list[0]) if isbn_list else "Unknown ISBN"

            # Year logic
            year_raw = book.get("first_publish_year")
            publish_year_value = str(year_raw) if year_raw else "N/A"


            # 2. Create the Book Object
            try:
                new_book = Book(
                    authors = authors,
                    isbn = isbn_value,
                    publish_year = publish_year_value,
                    title = book.get("title", "Untitled")
                )
                book_set.append(new_book)
            except Exception as e:
                print(f"Skipping a book due to validation error: {e}")
                continue

        # 3. Wrap in your Books collection model
        ret_books = Books(
            count = book_data.get("numFound", 0), # Open Library uses numFound
            books = book_set
        )

        return ret_books

    except requests.exceptions.RequestException as e:
        print(f"API Connection Error: {e}")
        # Return an empty collection instead of None to satisfy the Pydantic model
        return Books(count=0, books=[])


@app.get("/book/{isbn}", response_model=Book)
def get_book_details(isbn: str):
    OPEN_LIBRARY_URL_BASE = "https://openlibrary.org"

    OPEN_LIBRARY_URL_BOOK = OPEN_LIBRARY_URL_BASE + f"/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"

    response = requests.get(OPEN_LIBRARY_URL_BOOK)
    book_data = response.json()
    #raise HTTPException(status_code=404, detail=f"{data}")
# Open Library returns data keyed by the bibkey, e.g., 'ISBN:9780321765723'
    book_key = f"ISBN:{isbn}"
    data = book_data.get(book_key)
    if data.get("error"):
        # Handle case where ISBN is valid but no book is found
        raise HTTPException(status_code=404, detail=f"Book not found for ISBN: {OPEN_LIBRARY_URL_BOOK}")

    title = data.get("title")
    pub_date = data.get("publish_date")
    isbn10s = data.get("isbn_10")
    isbn13s = data.get("isbn_13")
    publishers = data.get("publishers")
    authors = data.get("authors")

    authors_info = set()

    for author in authors:
        authors_info.add(author.get("name"))






    book = Book(
        authors = authors_info,
        isbn = isbn,
        publish_year = pub_date,
        title = title)

    return book

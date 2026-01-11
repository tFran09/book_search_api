import requests
from typing import Optional, List, Dict, Any
from book_models import Book, Books
from urllib.parse import quote

# Define the base URL of your FastAPI application
API_BASE_URL = "http://127.0.0.1:8000"

class BookAPIClient:
    """
    A client class to handle all interactions with the local Book Lookup API.
    """
    
    def __init__(self, base_url: str = API_BASE_URL):
        """
        Initializes the client with the base URL.
        """
        self.base_url = base_url

    def search_books_by_title(self, title: str, exact: bool = False) -> Optional[Books]:
        """
        Performs a search request to the /search/{title} endpoint 
        and returns a list of book data dictionaries.
        
        Args:
            title: The search term (book title).

        Returns:
            A list of dictionaries containing book data, or None if the request fails.
        """
        
        # 1. Construct the full URL
        # We assume your search endpoint takes the title directly in the path
        # Note: In a real-world scenario, you might want to URL-encode the title
        search_endpoint = f"/search/{title}?exact={str(exact).lower()}"
        search_url = self.base_url + search_endpoint
        
        try:
            # 2. Make the HTTP GET request
            response = requests.get(search_url)
            
            # Raise an exception for HTTP errors (4xx or 5xx status codes)
            response.raise_for_status() 
            
            # 3. Parse the JSON response
            data = response.json()
            
            # 4. Extract the list of books from the response payload
            # Assuming your API response structure is {"count": N, "books": [...]}
            return Books.model_validate(data)            
        except requests.exceptions.RequestException as e:
            # Handle connection errors, timeouts, or HTTP status errors
            print(f"Error connecting to API or receiving response: {e}")
            return None

    def search_books_by_author(self, author_name: str, exact: bool = False) -> Optional[Books]:
        """
        Performs a search request to the /search/author/{author_name} endpoint 
        and returns a list of book data dictionaries.
        
        Args:
            author_name: The name of the author to search for.

        Returns:
            A list of dictionaries containing book data, or None if the request fails.
        """
        
        # 1. Construct the full URL
        # quote() handles spaces and special characters in names
        safe_author_name = quote(author_name)
        search_endpoint = f"/search/author/{safe_author_name}?exact={str(exact).lower()}"
        search_url = self.base_url + search_endpoint
        
        try:
            # 2. Make the HTTP GET request
            response = requests.get(search_url)
            
            # Raise an exception for HTTP errors (4xx or 5xx status codes)
            response.raise_for_status() 
            
            # 3. Parse the JSON response
            data = response.json()
            
            # 4. Extract and validate using your Pydantic model
            return Books.model_validate(data)            

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to API or receiving response: {e}")
            return None
        except Exception as e:
            # Catch validation errors if the data format doesn't match the model
            print(f"Data validation error: {e}")
            return None

    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        # 1. Construct the full URL
        # We assume your search endpoint takes the ISBN directly in the path
        book_endpoint = f"/book/{isbn}"
        book_url = self.base_url + book_endpoint
        
        try:
            # 2. Make the HTTP GET request
            response = requests.get(book_url)
            
            # Raise an exception for HTTP errors (4xx or 5xx status codes)
            response.raise_for_status() 
            
            # 3. Parse the JSON response
            data = response.json()
            # Return a single validated Book model
            return Book.model_validate(data) 
        except Exception as e:
            print(f"Error processing book details: {e}")
            return None

# --- Example Usage (Optional, for testing the client independently) ---
if __name__ == "__main__":
    client = BookAPIClient()
    search_term = "Moby Dick"
    print(f"Searching for: {search_term}...")
    
    books = client.search_books_by_title(search_term)
    
    if books:
        print(f"Found {len(books)} books.")
        print(books[0]) # Print the first result
    else:
        print("Search failed or returned no results.")
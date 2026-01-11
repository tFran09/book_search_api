# Book Search CLI

A command-line interface tool for searching books, viewing details, and managing a personal reading library.

## Overview

This application allows users to query a book database using an ISBN, Title, or Author. It features a local "Library" system where users can save books they own or want to read. It leverages **Pydantic** for data validation, **Tabulate** for formatted terminal output, and **TinyDB** for local storage.

## Prerequisites

- Python 3.7+

## Installation

1. Navigate to the project directory.

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

This application consists of a local API server and a CLI client. You need to run both.

1. **Start the API Server** (in a separate terminal):
   ```sh
   uvicorn book_api:app --reload
   ```

2. **Run the CLI Application**:

```sh
python book.py
```

### Search Options

1. **ISBN Search**: Enter `1` to search for a specific book by its ISBN.
2. **Title Search**: Enter `2` to search for books by title. The application will list the total count of results and display details for each match.
3. **Library Management**: View your collection, filter by "To Read", and mark books as read.

## Project Files

- `book_search_client.py`: Main script handling user input and display logic.
- `book_api_client.py`: Client for interacting with the Book API.
- `book_models.py`: Data models defining the structure of Book objects.
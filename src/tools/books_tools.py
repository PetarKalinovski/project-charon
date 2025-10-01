import sys
from pathlib import Path

from strands import tool

sys.path.append(str(Path(__file__).parent.parent))
import json
from datetime import datetime
from typing import Optional

import requests
from dotenv import load_dotenv
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.config_loader import load_config
from src.utils.callback_hanlder_subagents import log_to_session

load_dotenv()


@tool
def get_book_lists() -> str:
    """
    Get the complete book reading list and reading history.
    The agent will analyze this data to make personalized recommendations.

    Returns:
        str: JSON string containing full book data
    """
    config = load_config()
    book_paths = config.books_agent.book_list_file
    try:
        with open(book_paths) as f:
            books = json.load(f)

        total_to_read = len(books.get("to_read", []))
        total_read = len(books.get("read", []))

        result = f"BOOK DATA (To Read: {total_to_read}, Read: {total_read})\n"
        result += "=" * 50 + "\n\n"
        result += json.dumps(books, indent=2)

        return result
    except Exception as e:
        return f"Error reading book data: {str(e)}"


@tool
def add_book_to_reading_list(
    title: str,
    author: str,
    genre: Optional[str] = None,
    pages: Optional[int] = None,
    notes: Optional[str] = None,
) -> str:
    """
    Add a book to the reading list.

    Args:
        title: Book title
        author: Book author
        genre: Book genre/category
        pages: Number of pages
        notes: Any additional notes or why the user wants to read it

    Returns:
        str: Confirmation message
    """
    config = load_config()
    book_paths = config.books_agent.book_list_file
    try:
        with open(book_paths) as f:
            books = json.load(f)

        # Check if book already exists
        existing = next(
            (
                b
                for b in books["to_read"]
                if b["title"].lower() == title.lower()
                and b["author"].lower() == author.lower()
            ),
            None,
        )
        if existing:
            return f"'{title}' by {author} is already in your reading list!"

        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages,
            "notes": notes,
            "added_date": datetime.now().isoformat()[:10],
        }

        books["to_read"].append(new_book)

        with open(book_paths, "w") as f:
            json.dump(books, f, indent=2)

        log_to_session(f"Added '{title}' by {author} to your reading list!")

        return f"Added '{title}' by {author} to your reading list!"
    except Exception as e:
        log_to_session(f"Error adding book: {str(e)}")

        return f"Error adding book: {str(e)}"


@tool
def mark_book_read(
    title: str, author: str, rating: Optional[float] = None, notes: Optional[str] = None
) -> str:
    """
    Mark a book as read and move it to the read list.

    Args:
        title: Book title (must match existing title)
        author: Book author (must match existing author)
        rating: Your rating out of 10
        notes: Your thoughts about the book

    Returns:
        str: Confirmation message
    """
    config = load_config()
    book_paths = config.books_agent.book_list_file
    try:
        with open(book_paths) as f:
            books = json.load(f)

        # Find book in to_read list
        book_index = None
        for i, book in enumerate(books["to_read"]):
            if (
                book["title"].lower() == title.lower()
                and book["author"].lower() == author.lower()
            ):
                book_index = i
                break

        if book_index is None:
            return f"'{title}' by {author} not found in your reading list. Make sure both title and author match exactly."

        # Move book to read list
        read_book = books["to_read"].pop(book_index)
        read_book["read_date"] = datetime.now().isoformat()[:10]

        if rating is not None:
            read_book["rating"] = rating
        if notes:
            read_book["notes"] = notes

        books["read"].append(read_book)

        with open(book_paths, "w") as f:
            json.dump(books, f, indent=2)

        log_to_session(
            f"Marked '{title}' by {author} as read! {f'Rated {rating}/10. ' if rating else ''}Nice work!"
        )
        return f"Marked '{title}' by {author} as read! {f'Rated {rating}/10. ' if rating else ''}Nice work!"

    except Exception as e:
        log_to_session(f"Error marking book as read: {str(e)}")
        return f"Error marking book as read: {str(e)}"


@tool
def search_book(title: str, author: str = "") -> str:
    """
    Search for book information using the Open Library API.

    Args:
        title: Book title to search by
        author: Book author to search by (optional)

    Returns:
        str: A string of JSONs that the API matched to the search
    """
    api_url = "https://openlibrary.org/search.json"
    params = {"title": title}
    log_to_session(f"Searching Open Library for book: {title} (Author: {author})")
    if author:
        params["author"] = author

    try:
        response = requests.get(api_url, params=params)
        data = response.json()

        if data.get("numFound", 0) > 0:
            log_to_session(f"Open Library returned the following books {data}")

            return f"Found matches: {json.dumps(data)}"
        else:
            log_to_session("Book not found")
            return (
                f"Book '{title}' not found. Error: {data.get('Error', 'Unknown error')}"
            )

    except Exception as e:
        log_to_session(f"Error searching for book: {str(e)}")
        return f"Error searching for book: {str(e)}"

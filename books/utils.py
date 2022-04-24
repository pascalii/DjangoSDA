import math
from typing import List, Dict, Any

import requests
from logging import getLogger

from django.utils.dateparse import parse_date
from requests import RequestException, Response

from books.models import Book, BookAuthor, Category

google_logger = getLogger("GoogleLogger")


def get_books_from_google_api(query_arg: str = "*") -> List[Book]:
    """
    usage is here https://developers.google.com/books/docs/v1/using
        Pagination can be done by :
        'For any request for all items in a collection, you can paginate
        results by specifying startIndex and maxResults in the parameters for the request
        Default: maxResults=10
        Maximum allowable value: maxResults=40.'
    """
    print("run")
    books_volume_url = "https://www.googleapis.com/books/v1/volumes?q={query_arg}&startIndex={start}&maxResults={chunk_size}"
    books: List[Book] = []
    try:
        google_response: Response = requests.get(books_volume_url.format(query_arg=query_arg, start=0, chunk_size=1))
    except RequestException as e:
        # google_logger.error(f"Encounter error while requesting to google, more: {e.args}")
        print(f"Encounter error while requesting to google, more: {e.args}")
        return []
    else:
        if 200 <= google_response.status_code < 300:
            total: int = google_response.json()["totalItems"]
            for start_index in _generate_pagination(total):
                try:
                    print(start_index)
                    response: Response = requests.get(books_volume_url.format(query_arg=query_arg, start=start_index, chunk_size=40))
                except RequestException as e:
                    # google_logger.error(f"Encounter error while requesting to google, more: {e.args}")
                    print(f"Encounter error while requesting to google while pagination, more: {e.args}, start_index: {start_index}")
                    continue
                else:
                    results = response.json()
                    print(f"items.len={len(results.get('items', []))}")
                    for item in results.get("items", []):
                        try:
                            books.append(_build_book_from_item(item))
                        except:
                            continue
        else:
            # google_logger.error(f"Request of {google_response.url} has status = {google_response.status_code}")
            print(f"Request of {google_response.url} has status = {google_response.status_code}")
        return books


def _generate_pagination(total, start: int = 0, chunk_size: int = 40):
    chunks_number = math.ceil(total/chunk_size)
    for chunk_number in range(chunks_number):
        if chunk_number != 0:
            start = chunk_size * chunk_number
        yield start


def _build_book_from_item(item: Dict[str, Any]) -> Book:
    book_info: Dict[str, Any] = item["volumeInfo"]
    # update_or_create return tuple of [Object, IsCreated] - we need only object in that case
    authors = [BookAuthor.objects.update_or_create(name=author_name)[0] for author_name in book_info.get("authors", [])]
    categories = [Category.objects.update_or_create(name=category_name)[0] for category_name in book_info.get("authors", [])]
    book = Book.objects.update_or_create(
        title=book_info.get("title"),
        publisher=book_info.get("publisher"),
        published_date=parse_date(book_info.get("publishedDate")) if book_info.get("publishedDate") else None,
        average_rating=book_info.get("averageRating")
    )[0]
    book.authors.set([author.id for author in authors])
    book.categories.set([category.id for category in categories])
    return book
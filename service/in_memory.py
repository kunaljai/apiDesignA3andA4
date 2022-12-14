import os.path
import sys

sys.path.append(os.path.dirname(__file__) + "/..")
sys.path.append(os.path.dirname(__file__) + "/../service")

import grpc

import service.inventory_pb2 as inventory_pb2
from service.error import GRPCError


class InMemory:
    db = None
    error = None

    def __init__(self):
        """
        This class implements an in memory database using a python dictionary.
        """
        self.error = GRPCError()
        print("Initialized InMemory")
        self.db = dict()
        book1 = dict()
        book1['isbn'] = "isbn1"
        book1['title'] = "Rich Dad Poor Dad"
        book1['author'] = "Robert T. Kiyosaki"
        book1['genre'] = inventory_pb2.Book.GenreType.THRILLER
        book1['publishing_year'] = 2017
        self.db[book1['isbn']] = book1
        book2 = dict()
        book2['isbn'] = "isbn2"
        book2['title'] = "Untamed"
        book2['author'] = "Glennon Doyle"
        book2['genre'] = inventory_pb2.Book.GenreType.TRAGIC
        book2['publishing_year'] = 2020
        self.db[book2['isbn']] = book2
        book3 = dict()
        book3['isbn'] = "isbn3"
        book3['title'] = "Atomic Habits"
        book3['author'] = "James Clear"
        book3['genre'] = inventory_pb2.Book.GenreType.COMEDY
        book3['publishing_year'] = 2018
        self.db[book3['isbn']] = book3

    def add(self, book):
        """
        This method will add the book object from request to the database
        @param book:
        @return:
        """
        try:
            parsed_book = marshalling_into_book(book)
            print("Attempting to add marshalled book")
            if parsed_book['isbn'] in self.db.keys():
                return self.error.raise_error("ISBN already exists, cannot add book", )
            self.db[parsed_book['isbn']] = parsed_book
            return self.db[parsed_book['isbn']]['isbn']
        except Exception as e:
            return self.error.raise_error(str(e))

    def get(self, isbn):
        """
        This method returns a book from the database using the passed ISBN
        @param isbn:
        @return:
        """
        print("Fetching book from InMemory database")
        if not isinstance(isbn, str):
            return self.error.raise_error("Improper payload")
        if isbn not in self.db.keys():
            return self.error.raise_error("ISBN not found", grpc.StatusCode.NOT_FOUND)
        return self.db[isbn]


def marshalling_into_book(book):
    """
    This method takes data from the request object and converts it into storage object
    @param book:
    @return:
    """
    if str(type(book)) != str(type(inventory_pb2.Book())):
        raise Exception("Improper payload")
    parsed_book = dict()
    parsed_book['isbn'] = book.isbn
    parsed_book['title'] = book.title
    parsed_book['author'] = book.author
    parsed_book['publishing_year'] = book.publishing_year
    parsed_book['genre'] = book.genre
    return parsed_book

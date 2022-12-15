import os.path
import sys

sys.path.append(os.path.dirname(__file__) + "/..")
sys.path.append(os.path.dirname(__file__) + "/../service")

from concurrent import futures
from helper.configuration import Configuration

import grpc

import inventory_pb2
import inventory_pb2_grpc
from service.error import GRPCError
from service.in_memory import InMemory


class InventoryServicer(inventory_pb2_grpc.InventoryServiceServicer):
    dao = None

    def __init__(self):
        self.dao = InMemory()

    def GetBook(self, request, context):
        # Request validation
        error = validate_get_book_request(request)
        if error is not None:
            if isinstance(error, GRPCError):
                return set_error_context_and_return_empty(
                    context,
                    error.error_message,
                    error.error_code
                )
            else:
                return set_error_context_and_return_empty(
                    context,
                    str(error)
                )

        # Business logic
        print("Logging request: ")
        print(request)
        fetched_book = self.dao.get(request.isbn)
        if fetched_book is None or fetched_book is inventory_pb2.Book():
            return set_error_context_and_return_empty(
                context,
                "Book does not exists",
                grpc.StatusCode.NOT_FOUND
            )
        if isinstance(fetched_book, GRPCError):
            return set_error_context_and_return_empty(
                context,
                fetched_book.error_message,
                fetched_book.error_code
            )

        # Response marshalling
        response = inventory_pb2.GetBookResponse()
        response.isbn = fetched_book['isbn']
        response.title = fetched_book['title']
        response.author = fetched_book['author']
        response.genre = inventory_pb2.Book.GenreType.Name(fetched_book['genre'])
        response.publishing_year = fetched_book['publishing_year']
        return response

    def CreateBook(self, request, context):
        # Request validation
        error = validate_create_book_request(request)
        if error is not None:
            if isinstance(error, GRPCError):
                return set_error_context_and_return_empty(
                    context,
                    error.error_message,
                    error.error_code
                )
            else:
                return set_error_context_and_return_empty(
                    context,
                    str(error)
                )

        # Business logic
        print("Logging request: ")
        print(request)
        isbn = None
        try:
            isbn = self.dao.add(request.book)
        except Exception as e:
            return set_error_context_and_return_empty(
                context,
                str(e)
            )
        if isbn is None:
            return set_error_context_and_return_empty(
                context,
                "Book could not be added"
            )
        if isinstance(isbn, GRPCError):
            return set_error_context_and_return_empty(
                context,
                isbn.error_message,
                isbn.error_code
            )

        # Response marshalling
        response = inventory_pb2.CreateBookResponse()
        response.isbn = isbn
        return response


def serve():
    connection_string = Configuration.fetch_connection_details("SERVER")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryServicer(), server)
    server.add_insecure_port(connection_string)
    server.start()
    print("Server started")
    server.wait_for_termination()


def set_error_context_and_return_empty(context, error, status_code=None):
    context.set_details(error)
    context.set_code(status_code)
    if status_code is None:
        context.set_code(grpc.StatusCode.UNKNOWN)
    return inventory_pb2.GetBookResponse()


def validate_get_book_request(request):
    """
    This method validates whether the request sent to GetBook is valid
    @param request:
    @return:
    """
    if isinstance(request, inventory_pb2.GetBookRequest):
        isbn = request.isbn
        if isinstance(isbn, str):
            if isbn is not None and isbn != "":
                return None
    return GRPCError().raise_error(
        "Improper message",
        grpc.StatusCode.INVALID_ARGUMENT
    )


def validate_create_book_request(request):
    """
    This method validates whether the request sent to CreateBook is valid
    @param request:
    @return:
    """
    error_message = None
    try:
        if isinstance(request, inventory_pb2.CreateBookRequest):
            book = request.book
            if isinstance(book, inventory_pb2.Book):
                any_error = False
                if book.isbn is None or book.isbn == "":
                    error_message = "Improper ISBN"
                    any_error = True
                if book.title is None or book.title == "":
                    error_message = "Improper title"
                    any_error = True
                if book.author is None or book.author == "":
                    error_message = "Improper Author"
                    any_error = True
                if book.genre is None or book.genre not in inventory_pb2.Book.GenreType.values():
                    error_message = "Improper Genre"
                    any_error = True
                if book.publishing_year is None or book.publishing_year > 2022 or book.publishing_year < 1400:
                    error_message = "Improper Publishing Year"
                    any_error = True
                if not any_error:
                    return None
    except Exception as e:
        return GRPCError().raise_error(str(e))
    if error_message is not None:
        return GRPCError().raise_error(
            error_message,
            grpc.StatusCode.INVALID_ARGUMENT
        )
    return GRPCError().raise_error(
        "Improper message",
        grpc.StatusCode.INVALID_ARGUMENT
    )


if __name__ == '__main__':
    serve()

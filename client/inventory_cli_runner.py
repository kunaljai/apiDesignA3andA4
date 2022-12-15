import os.path
import sys

sys.path.append(os.path.dirname(__file__) + "/..")
sys.path.append(os.path.dirname(__file__) + "/../service")

import grpc

from service import inventory_pb2
from service import inventory_pb2_grpc
from helper.configuration import Configuration


# Feel free to ignore this file. This is just to test the APIs using CLI.


def run():
    connection_string = Configuration.fetch_connection_details("CLIENT")
    with grpc.insecure_channel(connection_string) as channel:
        stub = inventory_pb2_grpc.InventoryServiceStub(channel)
        print("Welcome to the library!")
        while True:
            try:
                print("1) Get book details by ISBN\n"
                      "2) Add a book to library\n"
                      "3) Exit\n"
                      "Please enter your choice: ", end="")
                choice = int(input())
                if choice == 1:
                    print("Please enter the ISBN (example, isbn1): ", end="")
                    isbn = str(input())
                    req = inventory_pb2.GetBookRequest()
                    req.isbn = isbn
                    response = stub.GetBook(req)
                    print('Response: ')
                    print(response)
                elif choice == 2:
                    print("Please enter the book's ISBN: ", end="")
                    isbn = str(input())
                    print("Please enter the book's title: ", end="")
                    title = str(input())
                    print("Please enter the book's author: ", end="")
                    author = str(input())
                    print("Please enter the book's genre from the options below "
                          "(enter the corresponding number, example: 0): ")
                    for i in inventory_pb2.Book.GenreType.values():
                        print(str(i) + ") " + inventory_pb2.Book.GenreType.Name(i))
                    genre = int(input())
                    print("Please enter the book's publishing year: ", end="")
                    year = int(input())
                    req = inventory_pb2.CreateBookRequest()
                    req.book.isbn = isbn
                    req.book.title = title
                    req.book.author = author
                    req.book.genre = genre
                    req.book.publishing_year = year
                    response = stub.CreateBook(req)
                    print("Response: ")
                    print(response)
                elif choice == 3:
                    break
                else:
                    print("Please enter a valid choice")
            except grpc.RpcError as e:
                print("An exception occurred")
                print(e)
                print("Please try again")
            except ValueError as ve:
                print("Please enter valid input, try again")


if __name__ == '__main__':
    run()

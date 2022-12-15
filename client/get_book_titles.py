import os.path
import sys

import grpc

sys.path.append(os.path.dirname(__file__) + "/..")
sys.path.append(os.path.dirname(__file__) + "/../service")

from client.inventory_client import Client
from helper.configuration import Configuration


def get_book_titles(client, isbn_list):
    titles = list()
    for isbn in isbn_list:
        book = client.get_book(isbn)
        if isinstance(book, Exception):
            err = grpc.RpcError(book)
            print(isbn + " -> " + get_details_from_rpc_error(err))
        elif book is not None and book.title is not None:
            titles.append(book.title)
        else:
            titles.append('')
    return titles


def get_details_from_rpc_error(err):
    try:
        err = str(err)
        start_ind = err.find("details") + 11
        end_ind = err.find("\"", start_ind)
        return err[start_ind:end_ind]
    except Exception as e:
        return "Unknown"


def run():
    # Readying the client
    client = Client()
    connection_string = Configuration.fetch_connection_details("CLIENT")
    client.connect_with_connection_string(connection_string)

    # Calling the method with 2 hardcoded ISBNs
    titles = get_book_titles(client, ['isbn1', 'isbn2'])

    # Printing the result
    print(titles)


if __name__ == '__main__':
    run()

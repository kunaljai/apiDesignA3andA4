import os.path
import sys
import unittest

sys.path.append(os.path.dirname(__file__) + "/..")
sys.path.append(os.path.dirname(__file__) + "/../service")

from client.inventory_client import Client
from client.get_book_titles import get_book_titles
from unittest.mock import MagicMock
from service import inventory_pb2
from helper.configuration import Configuration


class TestGetBookTitles(unittest.TestCase):
    def test_get_book_titles_mocked(self):
        client_mock = MagicMock()
        book1 = inventory_pb2.Book()
        book1.title = "Rich Dad Poor Dad"
        book2 = inventory_pb2.Book()
        book2.title = "Untamed"
        client_mock.get_book = MagicMock(side_effect=[book1, book2])
        titles = get_book_titles(client_mock, ['isbn1', 'isbn2'])
        client_mock.get_book.assert_any_call("isbn1")
        client_mock.get_book.assert_any_call("isbn2")
        assert titles == ['Rich Dad Poor Dad', 'Untamed']

    def test_get_book_titles_live(self):
        client_live = Client()
        connection_string = Configuration.fetch_connection_details("CLIENT")
        client_live.connect_with_connection_string(connection_string)
        titles = get_book_titles(client_live, ['isbn1', 'isbn2'])
        assert titles == ['Rich Dad Poor Dad', 'Untamed']


if __name__ == "__main__":
    unittest.main()

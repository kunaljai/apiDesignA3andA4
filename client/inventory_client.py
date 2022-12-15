import os.path
import sys

sys.path.append(os.path.dirname(__file__) + "/..")
sys.path.append(os.path.dirname(__file__) + "/../service")

import grpc

from service import inventory_pb2_grpc, inventory_pb2


class Client:
    host = None
    port = None
    channel = None
    stub = None

    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port

    def connect_with_connection_string(self, connection_string):
        self.channel = grpc.insecure_channel(connection_string)
        self.stub = inventory_pb2_grpc.InventoryServiceStub(self.channel)

    def connect(self):
        if self.host is None or self.port is None:
            print("Invalid host or port")
            pass
        connection_string = self.host + ":" + self.port
        self.connect_with_connection_string(connection_string)

    def get_book(self, isbn):
        try:
            request = inventory_pb2.GetBookRequest()
            request.isbn = isbn
            return self.stub.GetBook(request)
        except Exception as e:
            return e

    def create_book(self, book):
        try:
            request = inventory_pb2.CreateBookRequest(book)
            return self.stub.CreateBook(request)
        except Exception as e:
            print(e)
            return None

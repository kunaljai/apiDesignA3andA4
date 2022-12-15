import os
from configparser import ConfigParser


class Configuration:
    @staticmethod
    def fetch_connection_details(config_name):
        try:
            config = ConfigParser()
            path = os.path.dirname(__file__) + "/../resources/config.ini"
            config.read(path)
            connection = config[config_name]
            host = connection["host"]
            port = connection["port"]
            return host + ":" + port
        except Exception as e:
            print(e)
        return ""

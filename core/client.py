"""
client.py
"""

from .node import Node
from configparser import ConfigParser
import os


class Client(Node):

    def __init__(self,
                 host_name,
                 server,
                 directory):
        super(Client, self).__init__(directory=directory)
        self.host_name = host_name
        self.server = server
        self.directory = directory
        self.connect_to_server()

    def connect_to_server(self):
        config = ConfigParser()
        config['server'] = dict(address=self.directory)
        file_name = f".{self.host_name}.server.cfg"
        file_path = os.path.join(self.directory, file_name)
        with open(file_path, 'w+') as f:
            config.write(f)

        self.log(f"Started Client")
        self.rsync(file_path, self.server, delete=False, contents=False)

    def sync(self, file_path, file_name, **kwargs):
        self.log(f"Syncing with server ({self.server})")
        self.rsync(self.directory, self.server, delete=True, exclude='.*')

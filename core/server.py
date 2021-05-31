"""
server.py
"""

from .node import Node
from configparser import ConfigParser
from pathlib import Path


class Server(Node):

    def __init__(self,
                 host_name,
                 directory):

        super().__init__(directory=directory)

        self.nodes = []
        self.host_name = host_name
        self.directory = directory
        self.log(f"Started Server")

    def sync(self, file_path, file_name, event_types, **kwargs):
        if file_name.endswith('.server.cfg'):
            try:
                self.add_client(file_path, file_name)
            except KeyError:
                # if file deleted
                pass
        else:
            self.sync_with_clients()

    def add_client(self, file_path: str, file_name: str, **kwargs):

        # read configuration
        config = ConfigParser()
        config_path = Path(file_path) / file_name
        config.read(str(config_path))
        client_addr = config['server']['address']

        # add to nodes
        if client_addr not in self.nodes:
            self.nodes.append(client_addr)
        client_name = file_name.split('.server')[0]
        self.log(f"Connected to @{client_name}")

        # remove after use
        config_path.unlink()

    def sync_with_clients(self):
        self.log(f"Syncing with clients ({len(self.nodes)})")
        for node_addr in self.nodes:
            self.rsync(src=self.directory, dest=node_addr, delete=True)

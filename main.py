"""
main.py
"""

from core.client import Client
from core.server import Server
from pathlib import Path
import shutil

root = Path('sandbox')
shutil.rmtree(root, ignore_errors=True)
root.mkdir()

nodes = ['curie', 'einstein', 'vinci', 'newton']
for idx, node in enumerate(nodes):
    is_server = idx == 0
    node_path = root / node
    node_path.mkdir()

    config = dict(host_name=node, directory=str(node_path))
    Server(**config) if is_server \
        else Client(**config, server=root / nodes[0])

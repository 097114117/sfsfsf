"""
node.py

Base class for `Server` and `Client`.

"""

import subprocess
import logging
import threading

import inotify.adapters
from inotify.constants import IN_CREATE, IN_MOVED_TO, IN_DELETE, IN_MODIFY, IN_MOVED_FROM

from time import sleep


class Node:

    def __init__(self, directory):
        self.logger = logging.getLogger('nodes')

        self.mask = IN_CREATE | IN_MOVED_TO | IN_DELETE | IN_MODIFY | IN_MOVED_FROM
        self.directory = directory

        inotify_thread = threading.Thread(target=self.fs_trigger, name='trigger')
        inotify_thread.start()

    def fs_trigger(self):
        i = inotify.adapters.InotifyTree(self.directory, mask=self.mask)
        for event in i.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            sleep(.1)  # buffer time
            self.sync(file_path=path, file_name=filename, event_types=type_names)

    def log(self, msg, **kwargs):
        if hasattr(self, 'host_name'):
            c_cyan = '\u001b[36;1m'
            c_reset = '\u001b[0m'
            msg = f"{c_cyan}[{self.host_name:^10}]{c_reset}\t{msg}"
        self.logger.log(msg=msg, **kwargs, level=logging.WARNING)

    def sync(self, file_path, file_name, event_types, **kwargs):
        raise NotImplemented

    @staticmethod
    def rsync(src, dest,
              delete=False,
              include=None,
              exclude=None,
              contents=True):

        args = []
        if delete:
            args.append(f'--delete')
        if include:
            args.append(f"--include={include}")
        if exclude:
            args.append(f"--exclude={exclude}")

        subprocess.run(f"rsync -a {' '.join(args)}"
                       f" {src}{'/' if contents else ''} {dest}",
                       shell=True)

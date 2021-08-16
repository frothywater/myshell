import os
from io import StringIO
from typing import Optional

from myshell.command import Command


class DirectoryInfoCommand(Command):
    def __init__(self):
        super().__init__("dir")

    def run(self, args: list[str], input: Optional[StringIO]):
        path = os.getcwd() if len(args) == 0 else args[0]
        if not os.access(path, os.F_OK):
            self.error(f"not such file or directory: {path}")
            return
        if not os.path.isdir(path):
            self.error(f"not a directory: {path}")
            return
        for entry in os.listdir(path):
            self.log(f"{entry}  ")

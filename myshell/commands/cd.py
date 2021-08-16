import os
from typing import TextIO

from myshell.command import Command


class ChangeDirectoryCommand(Command):
    def __init__(self):
        super().__init__("cd", description="change directory", usage="cd <dir>")

    def execute(self, args: list[str], in_: TextIO, out: TextIO, err: TextIO):
        if len(args) > 0:
            path = args[0]
            if not os.access(path, os.F_OK):
                err.write(f"not such file or directory: {path}\n")
                return
            if not os.path.isdir(path):
                err.write(f"not a directory: {path}\n")
                return
            os.chdir(path)

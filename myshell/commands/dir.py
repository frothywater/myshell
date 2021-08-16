import os
from typing import TextIO

from myshell.command import Command


class DirectoryInfoCommand(Command):
    def __init__(self):
        super().__init__(
            "dir", description="list all files in directory", usage="dir [<path>]"
        )

    def execute(self, args: list[str], in_: TextIO, out: TextIO, err: TextIO):
        path = os.getcwd() if len(args) == 0 else args[0]
        if not os.access(path, os.F_OK):
            err.write(f"not such file or directory: {path}\n")
            return
        if not os.path.isdir(path):
            err.write(f"not a directory: {path}\n")
            return
        for entry in os.listdir(path):
            out.write(f"{entry}  ")
        out.write("\n")

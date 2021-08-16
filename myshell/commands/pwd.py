import os
from typing import TextIO

from myshell.command import Command


class PrintWorkingDirectoryCommand(Command):
    def __init__(self):
        super().__init__("pwd", description="print working directory", usage="pwd")

    def execute(self, args: list[str], in_: TextIO, out: TextIO, err: TextIO):
        out.write(os.getcwd() + "\n")

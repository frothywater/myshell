import os
from io import StringIO
from typing import Optional

from myshell.command import Command


class PrintWorkingDirectoryCommand(Command):
    def __init__(self):
        super().__init__("pwd")

    def run(self, args: list[str], input: Optional[StringIO]):
        self.log(os.getcwd())

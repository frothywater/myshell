import os
from io import StringIO
from typing import Optional

from myshell.command import Command, CommandResult


class PrintWorkingDirectoryCommand(Command):
    def __init__(self):
        super().__init__("pwd")

    def run(self, args: list[str], input: Optional[StringIO] = None) -> CommandResult:
        self.log(os.getcwd())
        return CommandResult(self.output)

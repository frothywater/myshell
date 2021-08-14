import os
from io import StringIO
from typing import Optional

from myshell.command import Command, CommandResult


class ChangeDirectoryCommand(Command):
    def __init__(self):
        super().__init__("cd")

    def run(self, args: list[str], input: Optional[StringIO] = None) -> CommandResult:
        if len(args) > 0:
            path = args[0]
            if not os.access(path, os.F_OK):
                self.error(f"not such file or directory: ${path}")
                return CommandResult(exit_code=1)
            if not os.path.isdir(path):
                self.error(f"not a directory: ${path}")
                return CommandResult(exit_code=1)
            os.chdir(path)
        return CommandResult()

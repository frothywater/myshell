import os

from myshell.command import Command
from myshell.context import Context


class ChangeDirectoryCommand(Command):
    def __init__(self):
        super().__init__("cd", description="change directory", usage="cd <dir>")

    def execute(self, args: list[str], context: Context):
        if len(args) > 0:
            path = args[0]
            if not os.access(path, os.F_OK):
                context.err.write(f"not such file or directory: {path}\n")
                return
            if not os.path.isdir(path):
                context.err.write(f"not a directory: {path}\n")
                return
            os.chdir(path)

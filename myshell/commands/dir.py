import os

from myshell.command import Command
from myshell.context import Context


class DirectoryInfoCommand(Command):
    def __init__(self):
        super().__init__(
            "dir", description="list all files in directory", usage="dir [<path>]"
        )

    async def execute(self, args: list[str], context: Context):
        path = os.getcwd() if len(args) == 0 else args[0]
        if not os.access(path, os.F_OK):
            context.error(f"not such file or directory: {path}\n")
            return
        if not os.path.isdir(path):
            context.error(f"not a directory: {path}\n")
            return
        for entry in os.listdir(path):
            context.write(f"{entry}  ")
        context.write("\n")
        context.close_all()

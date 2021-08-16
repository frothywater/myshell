import os

from myshell.context import Context

from myshell.command import Command


class DirectoryInfoCommand(Command):
    def __init__(self):
        super().__init__(
            "dir", description="list all files in directory", usage="dir [<path>]"
        )

    def execute(self, args: list[str], context: Context):
        path = os.getcwd() if len(args) == 0 else args[0]
        if not os.access(path, os.F_OK):
            context.err.write(f"not such file or directory: {path}\n")
            return
        if not os.path.isdir(path):
            context.err.write(f"not a directory: {path}\n")
            return
        for entry in os.listdir(path):
            context.out.write(f"{entry}  ")
        context.out.write("\n")

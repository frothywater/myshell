import os

from myshell.context import Context

from myshell.command import Command


class PrintWorkingDirectoryCommand(Command):
    def __init__(self):
        super().__init__("pwd", description="print working directory", usage="pwd")

    def execute(self, args: list[str], context: Context):
        context.out.write(os.getcwd() + "\n")

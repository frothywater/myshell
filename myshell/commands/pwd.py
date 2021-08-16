import os

from myshell.command import Command
from myshell.context import Context


class PrintWorkingDirectoryCommand(Command):
    def __init__(self):
        super().__init__("pwd", description="print working directory", usage="pwd")

    async def execute(self, args: list[str], context: Context):
        context.write(os.getcwd() + "\n")
        context.close_all()

import os

from myshell.context import Context

from myshell.command import Command


class ClearCommand(Command):
    def __init__(self):
        super().__init__("clr", description="clear console screen", usage="clr")

    def execute(self, args: list[str], context: Context):
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")

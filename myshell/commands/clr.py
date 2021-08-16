import os
from typing import TextIO

from myshell.command import Command


class ClearCommand(Command):
    def __init__(self):
        super().__init__("clr", description="clear console screen", usage="clr")

    def execute(self, args: list[str], in_: TextIO, out: TextIO, err: TextIO):
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")

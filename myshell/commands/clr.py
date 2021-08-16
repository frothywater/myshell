import os
from io import StringIO
from typing import Optional

from myshell.command import Command


class ClearCommand(Command):
    def __init__(self):
        super().__init__("clr", description="clear console screen", usage="clr")

    def run(self, args: list[str], input: Optional[StringIO]):
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")

import os
from io import StringIO
from typing import Optional

from myshell.command import Command, CommandResult


class ClearCommand(Command):
    def __init__(self):
        super().__init__("clr")

    def run(self, args: list[str], input: Optional[StringIO] = None) -> CommandResult:
        if os.name == "nt":
            _ = os.system("cls")
        else:
            _ = os.system("clear")
        return CommandResult()

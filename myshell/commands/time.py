from datetime import datetime
from io import StringIO
from typing import Optional

from myshell.command import Command, CommandResult


class TimeCommand(Command):
    def __init__(self):
        super().__init__("time")

    def run(self, args: list[str], input: Optional[StringIO] = None) -> CommandResult:
        self.log(datetime.now().strftime("%c"))
        return CommandResult(self.output)

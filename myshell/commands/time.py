from datetime import datetime
from typing import TextIO

from myshell.command import Command


class TimeCommand(Command):
    def __init__(self):
        super().__init__(
            "time", description="print current date and time", usage="time"
        )

    def execute(self, args: list[str], in_: TextIO, out: TextIO, err: TextIO):
        out.write(datetime.now().strftime("%c") + "\n")

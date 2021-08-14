from datetime import datetime
from io import StringIO
from typing import Optional

from myshell.command import Command


class TimeCommand(Command):
    def __init__(self):
        super().__init__("time")

    def run(self, args: list[str], input: Optional[StringIO]):
        self.log(datetime.now().strftime("%c"))

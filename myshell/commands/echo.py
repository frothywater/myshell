from io import StringIO
from typing import Optional

from myshell.command import Command


class EchoCommand(Command):
    def __init__(self):
        super().__init__("echo", description="print text", usage="echo <text>")

    def run(self, args: list[str], input: Optional[StringIO]):
        if len(args) > 0:
            self.log(args[0] + "\n")

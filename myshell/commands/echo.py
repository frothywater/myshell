from typing import TextIO

from myshell.command import Command


class EchoCommand(Command):
    def __init__(self):
        super().__init__("echo", description="print text", usage="echo <text>")

    def execute(self, args: list[str], in_: TextIO, out: TextIO, err: TextIO):
        if len(args) > 0:
            out.write(args[0] + "\n")
